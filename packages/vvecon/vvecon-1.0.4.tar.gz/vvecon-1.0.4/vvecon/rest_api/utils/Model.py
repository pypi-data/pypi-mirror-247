from vvecon.rest_api.utils import Abortion
from vvecon.rest_api.utils.Types import ALL_, DICT, BOOL, CURSOR, CON, LIST, ANY
import functools
from urllib.parse import unquote, quote
from mysql.connector.errors import ProgrammingError, InterfaceError, OperationalError, InternalError

__all__ = ("Model", "cover")


def cover(error: str):
    """
    This method is to handle errors & exceptions occurs
    :param error: Preferred error message if the process fails, that can be delivered to API client
    :return: Return either whatever the decorated function returns or the error message
    """

    def func(f):
        """
        This method will wrap the desired function with a wrapping tool
        :param f: Function to be wrapped around
        :return: Returns an object for whatever returning from the decorated function
        """

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            """
            This wrapper function will cover the function with base flow of the process
            :param args: arguments to be passed into the function
            :param kwargs: keywords to be passed into the function
            :return: Returns whatever returning from the decorated function
            """
            try:
                return f(*args, **kwargs)
            except (ProgrammingError, InterfaceError, InternalError, OperationalError, IndexError) as e:
                print("[ERROR: " + error.upper() + "]", e)
                return Abortion("SYSTEM:Something went wrong, " + error.lower())

        return wrapper

    return func


# -- Model -- #
class Model:

    @staticmethod
    def unquote(argument: ALL_) -> ALL_:
        return unquote(argument) if isinstance(argument, str) else argument

    @staticmethod
    def quote(**kwargs):
        return {key: quote(value) if isinstance(value, str) else value for key, value in kwargs.items()}

    @staticmethod
    def parse(dictionary: dict, key: str):
        return dictionary[key] if key in dictionary.keys() else ""

    def build_condition(self, args: LIST = None, quote_args: LIST = None):
        conditions = []
        if args is not None:
            conditions.append(*[self.validate_input(*arg) for arg in args if type(arg) == list and len(arg) == 3])
        if quote_args is not None:
            conditions.append(
                *[self.validate_input(
                    arg[0], arg[1], quote(arg[2]) if isinstance(arg[2], str) else arg[2])
                    for arg in quote_args if type(arg) == list and len(arg) == 3]
            )
        return "AND".join(self.clens(conditions)) if len(conditions) else ""

    @staticmethod
    def validate_input(alias: str, column_name: str, value: ANY) -> str:
        return f"{alias}.`{column_name}` = '{value}'" if (
                value is not None and value != "" and value is not False and value != 0) else ""

    @staticmethod
    def clens(data: list) -> list:
        while "" in data:
            data.remove("")
        return data

    @staticmethod
    def get(cursor: CURSOR) -> BOOL:
        """
        This method gives True if the sql has returned a positive data or else False
        :param cursor: Database connection cursor
        :return: Returns True if the result contain positive data or else False
        """
        return False if len(cursor.fetchall()) == 0 else True

    def get_one(self, cursor: CURSOR) -> ALL_:
        """
        This method gives reserved value which was taken through sql code or else False if empty
        :param cursor: Database connection cursor
        :return: Returns a single data (One value) or else False
        """
        result = cursor.fetchall()
        return False if len(result) == 0 else self.unquote(result[0][0])

    def get_row_data(self, cursor: CURSOR) -> DICT:
        """
        This method gives reserved data dictionary or else False if empty
        :param cursor: Database connection cursor
        :return: Returns a set of data dictionary (One row) or else False if empty
        """
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        columns = cursor.description
        return {columns[index][0]: self.unquote(value) for index, value in enumerate(result[0])}

    def get_column_data(self, cursor: CURSOR) -> LIST:
        """
        This method gives reserved array of data containing a single column information
        :param cursor: Database connection cursor
        :return: Returns an array of data (One Column) or else False if empty
        """
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        return [self.unquote(value[0]) for value in result]

    def get_dict(self, cursor: CURSOR) -> DICT:
        """
        This method gives a dictionary of data of key and value columns combined or else False if empty
        :param cursor: Database connection cursor
        :return: Returns a dictionary of key, value column data or else False if empty
        """
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        return {key: self.unquote(value) for key, value in result}

    def get_data(self, cursor: CURSOR) -> LIST:
        """
        This method gives reserved array of data dictionaries or else False if empty
        :param cursor: Database connection cursor
        :return: Returns a set of array contains data dictionaries (Many rows) or else False if empty
        """
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        columns = cursor.description
        return [{columns[index][0]: self.unquote(value) for index, value in enumerate(result[row])}
                for row in range(len(result))]

    @staticmethod
    def commit(con: CON) -> BOOL:
        """
        This method commit the data to the MySQL server
        :param con: Database connection
        :return: Returns True if the committing succeed
        """
        con.commit()
        return True

    def execute(self, cursor: CURSOR, query: str, args: DICT = None, quote_args: DICT = None):
        if args is None:
            args = {}
        if quote_args is None:
            quote_args = {}
        cursor.execute(query.format(**args, **self.quote(**quote_args)))
