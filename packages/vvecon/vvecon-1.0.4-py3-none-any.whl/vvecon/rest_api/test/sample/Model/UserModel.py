from vvecon.rest_api.utils.Model import Model, cover
from vvecon.rest_api.utils.Types import CURSOR, CON, ALL_
from vvecon.rest_api.utils import Abortion
import pytz


# -- User Model -- #
class UserModel(Model):
    TIME_ZONE = pytz.timezone('America/New_York')
