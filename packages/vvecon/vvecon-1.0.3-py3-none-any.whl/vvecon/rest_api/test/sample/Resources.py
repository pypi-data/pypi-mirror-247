from vvecon.rest_api.utils import Router, Mail
from vvecon.rest_api.socket import SocketIO
from vvecon.rest_api.connections import get_connection
from Parsers.UserParser import UserParser
from Controller.UserController import UserController
from dotenv import load_dotenv
from os import environ

sock = SocketIO()
mail = Mail()

__all__ = ['User', 'sock', 'mail']

# load ENV
load_dotenv()

# initialize database connection
server_name = environ.get("SERVER")
database = environ.get("DATABASE")
user_name = environ.get("USER_NAME")
password = environ.get("PASSWORD")
db = get_connection(server_name, database, user_name, password)


# -- HOSTS -- #
USER = environ.get("USER")


# -- User Router -- #
class User(Router):
    # api keys by their host
    API_KEYS = {
        USER: environ.get("USER_API_KEY")
    }

    # pre created privileges attribute
    PRIVILEGES = {
        USER: {
            "example"
        }
    }

    # Initializing parser
    ARGS_PARSER = UserParser()

    # initialize controller
    CONTROLLER = UserController(db, mail)
