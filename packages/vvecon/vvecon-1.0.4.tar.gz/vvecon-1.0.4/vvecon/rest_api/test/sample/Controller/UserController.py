from vvecon.rest_api.utils import Mail
from vvecon.rest_api.utils.Controller import Controller, cover
from vvecon.rest_api.utils.Types import NONE, OBJ_, ANY, CURSOR, CON
from Model.UserModel import UserModel
import pytz


# -- GLOBAL VARS -- #
TIME_ZONE = pytz.timezone('America/New_York')


# -- User Controller -- #
class UserController(Controller):
    def __init__(self, db: OBJ_, mail: Mail = None) -> NONE:
        # initialize database connections
        self.db = db
        # initialize mail service
        self.__class__.MAIL = mail
        # initialize user model
        self.user_model = UserModel()
