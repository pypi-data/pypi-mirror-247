import functools
import inspect
from vvecon.rest_api.utils.Types import CURSOR, ANY
from vvecon.rest_api.utils.Abort import Abortion

__all__ = ("Controller", "cover")


def cover(error: str):
    """
    This function will cover the error handling part on Controllers
    :param error: Error message to be sent out from the API
    :return: Returns an object or whatever returning from the decorated function
    """
    def func(f):
        """
        This method will wrap the desired function with a wrapping tool
        :param f: Function to be wrapped around
        :return: Returns an object for whatever returning from the decorated function
        """
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            """
            This wrapper function will cover the function with base flow of the process
            :param self: Controller itself
            :param args: arguments to be passed into the function
            :param kwargs: keywords to be passed into the function
            :return: Returns whatever returning from the decorated function
            """
            with self.db as con:
                cursor: CURSOR = con.cursor()
                try:
                    con_required = 'con' in inspect.signature(f).parameters
                    if con_required:
                        return f(self, *args, **kwargs, con=con, cursor=cursor)
                    if not con_required:
                        return f(self, *args, **kwargs, cursor=cursor)
                except Exception as e:
                    print("[FAILED: " + error.upper() + "]", e)
                    return Abortion("SYSTEM:"+error.lower())
                finally:
                    cursor.close()
                    con.close()

        return wrapper

    return func


# -- Controller -- #
class Controller:
    # To be defined
    MAIL = None

    @staticmethod
    def check(result: ANY, check: ANY = None) -> ANY:
        return result == check or type(result) == Abortion

    @staticmethod
    def failed(result: ANY, message: str = "Operation failed", code: int = 404) -> ANY:
        return result if type(result) == Abortion else Abortion(message, code=code)

    def send_email(self, recipients: list, subject: str = "", body: str = ""):
        try:
            return self.__class__.MAIL.send(recipients, subject, body)
        except Exception as e:
            print("[MAIL FAILED: ", e, "]")
            return Abortion("VRAError 007: Failed to send the mail")
