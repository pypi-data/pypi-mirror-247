from flask_restful import Resource
from vvecon.rest_api.utils import Parser, Controller
from vvecon.rest_api.utils.Types import ANY_
from vvecon.rest_api.utils.Abort import *
from urllib.parse import unquote
from flask import jsonify
from flask_cors import cross_origin
import inspect


class Router(Resource):
    # To be defined
    API_KEYS: dict = None  # api keys by their host
    PRIVILEGES: dict = None  # pre created privileges attribute
    ARGS_PARSER: Parser = None  # Initializing parser
    CONTROLLER: Controller = None  # initialize controller

    ALL_PRIVILEGES = None  # will be created automatically when called

    def __init__(self) -> NONE:
        super(Router, self).__init__()
        self.__class__.ALL_PRIVILEGES = self.get_all_privileges()

    def get_all_privileges(self) -> list:
        # return list(set(key for inner_dict in self.__class__.PRIVILEGES.values() for key in inner_dict.keys() if key))
        return list(set(privilege for host in self.__class__.PRIVILEGES for privilege in self.PRIVILEGES[host]))

    def filter_args(self, func: str, args: dict) -> dict:
        """
        This filter the args dictionary according to the need of arguments required by the controller function.
        :param func: Name of controller function
        :param args: arguments given by api
        :return: returns a filtered dictionary fits for the controller function
        """
        data = dict()
        params = inspect.signature(self.__class__.CONTROLLER.__getattribute__(func)).parameters
        exceptions = ("cursor", "con")
        for param in params.values():
            if param.name not in exceptions:
                if (str(param.default) == "<class 'inspect._empty'>" and param.name not in args
                        and param.annotation != str):
                    abort_controller_missing_arg(param.name)
                if param.name not in args and param.annotation == str:
                    data[param.name] = ""
                if param.name in args and type(args[param.name]) != param.annotation:
                    abort_controller_arg_type_error(param.name)
                if param.name in args:
                    data[param.name] = args[param.name]
        return data

    # validate the host
    def validate_host(self, host: str, api_key: str) -> None:
        # check if the host is known
        if host not in self.__class__.API_KEYS.keys():
            abort_wrong_host()
        # check if the aoi key is correct for the current host
        if api_key != self.__class__.API_KEYS[host]:
            abort_wrong_api_key()

    # act on post method
    @cross_origin(origins="*")
    def post(self, action: str) -> object:
        # getting string normal form of itself
        action = unquote(action)
        # check if the action is valid
        if action not in self.__class__.ALL_PRIVILEGES:
            abort_invalid_method()
        # bind action with '_'
        func = "_".join(action.split(" "))
        # parsing arguments from header
        if hasattr(self.ARGS_PARSER, func):
            args = self.ARGS_PARSER.__getattribute__(func).parse_args(strict=True)
        # parse with the default parser if no dedicated parser
        else:
            args = self.ARGS_PARSER.default_require_args.parse_args(strict=True)
        # check if the host is authorized
        self.validate_host(args['host'], args['api_key'])
        # check if the action is a privilege of the current host
        if action not in self.__class__.PRIVILEGES[args['host']]:
            abort_invalid_method()
        # take the action and return the results
        if hasattr(self, func):
            if 'args' in inspect.signature(self.__getattribute__(func)).parameters:
                return jsonify(result=self.__getattribute__(func)(args)), 201
            if 'args' not in inspect.signature(self.__getattribute__(func)).parameters:
                return jsonify(result=self.__getattribute__(func)()), 201
        # follow default procedure if not dedicated resource function
        if not hasattr(self, func):
            return jsonify(result=self.__default__(func, args)), 201

    @staticmethod
    def abort(result) -> NONE:
        # TOO OLD getattr(globals(), self.__class__.PRIVILEGES[args['host']][action])(result)
        # OLD self.__class__.PRIVILEGES[args['host']][action](result)
        default_abort(result)

    def __default__(self, func: str, args: dict) -> ANY_:
        result = self.__class__.CONTROLLER.__getattribute__(func)(**self.filter_args(func, args))
        self.abort(result)
        return result
