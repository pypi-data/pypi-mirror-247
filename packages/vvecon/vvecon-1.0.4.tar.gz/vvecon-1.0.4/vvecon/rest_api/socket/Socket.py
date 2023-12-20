from flask import request
from flask_socketio import Namespace
from vvecon.rest_api.socket.SockAbort import *
from vvecon.rest_api.utils.Types import ANY_, DICT
import inspect


class Socket(Namespace):
    # To be defined
    API_HOSTS: list = None  # all the hosts which has access to the resource of Admin
    API_KEYS: dict = None  # api keys by their host
    ARGS_PARSER = None  # Initializing parser
    CONTROLLER = None  # initialize controller
    namespace_name = None  # initialize Namespace

    def filter_args(self, func: str, args: dict) -> dict:
        """
        This filter the args dictionary according to the need of arguments required by the controller function.
        :param func: Name of controller function
        :param args: arguments given by api
        :return: returns a filtered dictionary fits for the controller function
        """
        data = dict()
        params = inspect.signature(self.__class__.CONTROLLER.__getattribute__(func)).parameters
        for param in params.values():
            if str(param.default) == "<class 'inspect._empty'>" and param.name not in args and param.annotation != str:
                emit_controller_missing_arg(param.name, args['socket_id'])
            if param.name not in args and param.annotation == str:
                data[param.name] = ""
            if param.name in args and type(args[param.name]) != param.annotation:
                emit_controller_arg_type_error(param.name, args['socket_id'])
            if param.name in args:
                data[param.name] = args[param.name]
        return data

    # validate the host
    def validate_host(self, host: str, api_key: str, socket_id: str) -> bool:
        # check if the host is known
        if host not in self.__class__.API_HOSTS:
            emit_wrong_host(socket_id)
            return False
        # check if the aoi key is correct for the current host
        if api_key != self.__class__.API_KEYS[host]:
            emit_wrong_api_key(socket_id)
            return False
        return True

    @staticmethod
    def check(arg):
        return type(arg) == Abortion

    @staticmethod
    def failed(arg):
        default_emit(arg, request.sid)
        return False

    def main(self, action: str, req, proceed=True) -> DICT:
        # bind action with '_'
        func = "_".join(action.split(" "))
        # parsing arguments from header
        if hasattr(self.ARGS_PARSER, func):
            args = self.__class__.ARGS_PARSER.__getattribute__(action).parse_args(req, strict=False)
        # parse with the default parser if no dedicated parser
        else:
            args = self.ARGS_PARSER.default_socket_require_args.parse_args(strict=False)

        if 'socket_id' not in args:
            args['socket_id'] = request.sid

        if self.check(args):
            return self.failed(args)

        # check if the host is authorized
        valid_host = self.validate_host(args['host'], args['api_key'], request.sid)
        if self.check(valid_host):
            return self.failed(valid_host)

        if proceed:
            return self.__default__(func, args)
        return args

    def __default__(self, func: str, args: dict) -> ANY_:
        result = self.__class__.CONTROLLER.__getattribute__(func)(**self.filter_args(func, args))
        if result is not False:
            print("FUN:", func, "\nRES:", result)
            default_emit(result, args['socket_id'])
            if self.check(result):
                return self.failed(result)
            return result
        return False

    @staticmethod
    def load_args(data):
        data['socket_id'] = request.sid
        return data

    def on_connect(self, data):
        # try:
        #     print("GOT HERE", request.sid)
        #     self.emit("connect", room=request.sid, namespace=self.namespace_name)
        # except Exception as e:
        #     print("CON ERR", e)
        pass

    def on_login(self, data):
        args = self.load_args(data)
        print("LOGGED IN")
        if not self.check(args) and self.main("connect", args):
            emit("login", {"message": "You are logged in", "socket_id": args['socket_id']},
                 room=args['socket_id'], namespace=self.namespace_name)

    def on_logout(self, data):
        args = self.load_args(data)
        if not self.check(args):
            self.main("disconnect", args)

    def on_disconnect(self):
        try:
            self.disconnect(request.sid, self.namespace_name)
        except Exception as e:
            print("DIS ERR", e)
