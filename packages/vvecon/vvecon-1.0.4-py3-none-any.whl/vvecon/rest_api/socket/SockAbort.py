from flask_socketio import emit
from vvecon.rest_api.utils.Types import NONE, BONE
from vvecon.rest_api.utils.Abort import Abortion as VAbortion


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
            raise Exception("VRA001 Error: Invalid return code,", code)
        return True

    def emit(self, sid: str) -> NONE:
        emit('abort', {'code': self.code, 'message': self.message}, room=sid)


def default_emit(result, sid: str) -> NONE:
    if type(result) is Abortion:
        result.emit(sid)
    if type(result) is VAbortion:
        Abortion(result.message, result.code).emit(sid)


def default_empty_emit(result, abortion: Abortion, sid: str) -> NONE:
    if type(result) is bool and result is False:
        abortion.emit(sid)
    if type(result) is Abortion:
        result.emit(sid)


def emit_wrong_host(sid: str) -> NONE:
    Abortion("Invalid host information.", 403).emit(sid)


def emit_wrong_api_key(sid: str) -> NONE:
    Abortion("Incorrect api key.", 401).emit(sid)


def emit_invalid_method(sid: str) -> NONE:
    Abortion("Requested method not found.", 405).emit(sid)


def emit_controller_missing_arg(arg, sid: str) -> NONE:
    Abortion(arg+": Controller missing an argument on parser.", 400).emit(sid)


def emit_controller_arg_type_error(arg, sid: str) -> NONE:
    Abortion(arg+": Controller argument type doesn't match with the parser.", 400).emit(sid)
