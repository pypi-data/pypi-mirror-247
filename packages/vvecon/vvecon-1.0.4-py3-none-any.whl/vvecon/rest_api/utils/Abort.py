from flask_restful import abort
from vvecon.rest_api.utils.Types import NONE, BONE


class Abortion:
    code: int = 404
    message: str = None
    codes: list = [200, 201, 400, 401, 402, 403, 404, 405, 409, 500, 503]

    def __init__(self, message: str, code: int = 404) -> NONE:
        self.__validate_code__(code)
        self.code = code
        self.message = message

    def __validate_code__(self, code: int) -> BONE:
        if code not in self.__class__.codes:
            raise Exception("VRAError 001: Invalid return code,", code)
        return True

    def abort(self) -> NONE:
        abort(self.code, message=self.message)


# -- abort functions -- #

# default abortion for 404 error
def default_abort(result) -> NONE:
    if type(result) is Abortion:
        result.abort()


# default abortion for custom errors
def default_empty_abort(result, abortion: Abortion) -> NONE:
    if type(result) is bool and result is False:
        abortion.abort()
    if type(result) is Abortion:
        result.abort()


# abort if host is incorrect
def abort_wrong_host() -> NONE:
    Abortion("VRAError 002: Invalid host information.", 403).abort()


# abort if api key is incorrect
def abort_wrong_api_key() -> NONE:
    Abortion("VRAError 003: Incorrect api key.", 401).abort()


# abort if requested an invalid method
def abort_invalid_method() -> NONE:
    Abortion("VRAError 004: Requested method not found.", 405).abort()


# abort if failed to provide controller required arguments
def abort_controller_missing_arg(arg) -> NONE:
    Abortion("VRAError 005: "+arg+": Controller missing a argument on parser.", 400).abort()


# abort if controller argument required type doesn't match with the parser provided
def abort_controller_arg_type_error(arg) -> NONE:
    Abortion("VRAError 006: "+arg+": Controller argument type doesn't match with the parser.", 400).abort()
