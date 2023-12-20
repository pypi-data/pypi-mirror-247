from flask_restful.reqparse import RequestParser
from vvecon.rest_api.utils.Types import LIST, str__, NONE, OBJET

__all__ = ("ReqParser", "Parser")


# -- ReqParser -- #
class ReqParser(RequestParser):
    """
    This is to extend the RequestParser and simply the process for the dev
    """

    def __init__(self) -> NONE:
        super(ReqParser, self).__init__()
        self.add_arg("host", str__)
        self.add_arg("api_key", str__)

    # replacement function for add_argument to simply the procedure
    def add_arg(self, name: str, __type: OBJET, required: bool = True, choices: LIST = None) -> NONE:
        if choices is not None:
            self.add_argument(name, type=__type, help=name + " is required", required=required, trim=True,
                              nullable=(not required), choices=choices)
        if choices is None:
            self.add_argument(name, type=__type, help=name + " is required", required=required, trim=True,
                              nullable=(not required))


# -- Parser -- #
class Parser:
    default_require_args = ReqParser()
