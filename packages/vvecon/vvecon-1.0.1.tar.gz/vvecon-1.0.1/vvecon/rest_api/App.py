from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from vvecon.rest_api.socket import SocketIO
from vvecon.rest_api.utils import Mail
from vvecon.rest_api.utils.Types import NONE


class App(Flask):
    SOCK = None
    MAIL = None

    def __init__(self, *args, **kwargs) -> NONE:
        # initialize Flask Rest API
        super(App, self).__init__(*args, **kwargs)
        self.CORS = CORS(self)
        self.API = Api(self)

    def add_resource(self, resource, *urls, **kwargs) -> NONE:
        self.API.add_resource(resource, *[url+"<string:action>" for url in urls], **kwargs)

    def mail(self, mail: Mail, email: str, password: str) -> NONE:
        self.__class__.MAIL = mail
        self.__class__.MAIL.init_app(self)
        self.config['MAIL_SERVER'] = 'smtp.gmail.com'
        self.config['MAIL_PORT'] = 465
        self.config['MAIL_USERNAME'] = email
        self.config['MAIL_PASSWORD'] = password
        self.config['MAIL_USE_TLS'] = False
        self.config['MAIL_USE_SSL'] = True

    def socket(self, sock: SocketIO, mode=""):
        """
        :params sock: SocketIO object which defines in Resources
        :params mode: async modes - eventlet
        """
        self.__class__.SOCK = sock
        if mode != "":
            self.__class__.SOCK.init_app(self, async_mode=mode)
        if mode == "":
            self.__class__.SOCK.init_app(self)

    def run(self, debug: bool = False, port: int = 5000, **kwargs):
        if self.__class__.SOCK is not None:
            super(App, self).run(debug=debug, port=port, **kwargs)
            return
        super(App, self).run(debug=debug, port=port)
