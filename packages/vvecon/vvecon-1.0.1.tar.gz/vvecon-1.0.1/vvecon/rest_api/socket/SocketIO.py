from flask_socketio import SocketIO as socketIO


class SocketIO(socketIO):
    MODE = None

    def __init__(self, *args, **kwargs):
        super(SocketIO, self).__init__(*args, **kwargs)

    def init_app(self, app, **kwargs):
        if "async_mode" in kwargs:
            self.__class__.MODE = kwargs["async_mode"]
        super(SocketIO, self).init_app(app, **kwargs)

    def run(self, app, host: str = "0.0.0.0", debug: bool = False, port: int = 8000, **kwargs):
        if self.__class__.MODE == "eventlet":
            import eventlet
            eventlet.wsgi.server(eventlet.listen((host, port)), self)
            return
        if "allow_unsafe_werkzeug" in kwargs:
            kwargs.pop("allow_unsafe_werkzeug")
        super(SocketIO, self).run(debug=debug, port=port, allow_unsafe_werkzeug=True, **kwargs)
