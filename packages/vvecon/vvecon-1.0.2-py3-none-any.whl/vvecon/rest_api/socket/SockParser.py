from typing import MutableSequence
from flask import request, current_app
from flask_restful.reqparse import RequestParser, Argument
from vvecon.rest_api.utils.Types import NONE, str__, OBJET, LIST
from vvecon.rest_api.socket.SockAbort import Abortion
import six


_friendly_location = {
    u'json': u'the JSON body',
    u'form': u'the post body',
    u'args': u'the query string',
    u'values': u'the post body or the query string',
    u'headers': u'the HTTP headers',
    u'cookies': u'the request\'s cookies',
    u'files': u'an uploaded file',
}


class SocketArgument(Argument):
    unparsed_arguments = {}

    def source(self, req):
        return req

    def parse(self, req, bundle_errors=False):
        """Parses argument value(s) from the request, converting according to
        the argument's type.

        :param req: The flask request object to parse arguments from
        :param bundle_errors: Do not abort when first error occurs, return a
            dict with the name of the argument and the error message to be
            bundled
        """
        source = self.source(req)
        self.unparsed_arguments = req

        results = []

        # Sentinels
        _not_found = False
        _found = True

        for operator in self.operators:
            name = self.name + operator.replace("=", "", 1)
            if name in source:
                # Account for MultiDict and regular dict
                if hasattr(source, "getlist"):
                    values = source.getlist(name)
                else:
                    values = source.get(name)
                    if not (isinstance(values, MutableSequence) and self.action == 'append'):
                        values = [values]

                for value in values:
                    if hasattr(value, "strip") and self.trim:
                        value = value.strip()
                    if hasattr(value, "lower") and not self.case_sensitive:
                        value = value.lower()

                        if hasattr(self.choices, "__iter__"):
                            self.choices = [choice.lower()
                                            for choice in self.choices]
                    try:
                        value = self.convert(value, operator)
                    except Exception as error:
                        if self.ignore:
                            continue
                        return self.handle_validation_error(error, bundle_errors)

                    if self.choices and value not in self.choices:
                        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
                            return self.handle_validation_error(
                                ValueError(u"{0} is not a valid choice".format(
                                    value)), bundle_errors)
                        self.handle_validation_error(
                                ValueError(u"{0} is not a valid choice".format(
                                    value)), bundle_errors)

                    if name in self.unparsed_arguments:
                        self.unparsed_arguments.pop(name)
                    results.append(value)

        if not results and self.required:
            if isinstance(self.location, six.string_types):
                error_msg = u"Missing required parameter in {0}".format(_friendly_location.get(self.location,
                                                                                               self.location))
            else:
                friendly_locations = [_friendly_location.get(loc, loc) for loc in self.location]
                error_msg = u"Missing required parameter in {0}".format(' or '.join(friendly_locations))
            if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
                return self.handle_validation_error(ValueError(error_msg), bundle_errors)
            return self.handle_validation_error(ValueError(error_msg), bundle_errors)

        if not results:
            if callable(self.default):
                return self.default(), _not_found
            else:
                return self.default, _not_found

        if self.action == 'append':
            return results, _found

        if self.action == 'store' or len(results) == 1:
            return results[0], _found
        return results, _found

    def handle_validation_error(self, error, bundle_errors):
        """Called when an error is raised while parsing. Aborts the request
        with a 400 status and an error message

        :param error: the error that was raised
        :param bundle_errors: do not abort when first error occurs, return a
            dict with the name of the argument and the error message to be
            bundled
        """
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        msg = {self.name: error_msg}

        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, msg
        return Abortion(msg[0] if type(msg) is list else str(msg), code=400), False


class SockParser(RequestParser):
    unparsed_arguments = {}

    def __init__(self, socket_id: bool = True) -> NONE:
        super(SockParser, self).__init__()
        self.argument_class = SocketArgument
        self.add_arg("host", str__)
        self.add_arg("api_key", str__)
        if socket_id:
            self.add_arg("socket_id", str__)

    def add_argument(self, *args, **kwargs):
        """Adds an argument to be parsed.

        Accepts either a single instance of Argument or arguments to be passed
        into :class:`Argument`'s constructor.

        See :class:`Argument`'s constructor for documentation on the
        available options.
        """

        if len(args) == 1 and isinstance(args[0], self.argument_class):
            self.args.append(args[0])
        else:
            self.args.append(self.argument_class(*args, **kwargs))

        # Do not know what other argument classes are out there
        if self.trim and self.argument_class is SocketArgument:
            # enable trim for appended element
            self.args[-1].trim = kwargs.get('trim', self.trim)

        return self

    # replacement function for add_argument to simply the procedure
    def add_arg(self, name: str, __type: OBJET, required: bool = True, choices: LIST = None) -> NONE:
        if choices is not None:
            self.add_argument(name, type=__type, help=name + " is required", required=required, trim=True,
                              nullable=(not required), choices=choices)
        if choices is None:
            self.add_argument(name, type=__type, help=name + " is required", required=required, trim=True,
                              nullable=(not required))

    def parse_args(self, req=None, strict=False, http_error_code=400):
        if req is None:
            req = request

        namespace = self.namespace_class()
        self.__class__.unparsed_arguments = req

        # A record of arguments not yet parsed; as each is found
        # among self.args, it will be popped out
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                namespace[arg.dest or arg.name] = value
        if errors:
            return Abortion("Error while parsing args", code=400)

        if strict and req:
            return Abortion('Unknown arguments: %s' % ', '.join(self.__class__.unparsed_arguments.keys()), code=400)
        return namespace


# -- Socket Parser -- #

class SocketParser:
    default_socket_require_args = SockParser()
