import mysql
import logging
from mysql import connector
from vvecon.rest_api.utils.Types import NONE, CON


class DBConnection:
    def __init__(self, server_name: str = "", database: str = "", user_name: str = "", password: str = "",
                 attempts: int = 2, delay: int = 100, pool_size: int = 32) -> NONE:
        """
        Setup all the required variables in order to keep the DB connection
        """

        # CONFIGURE DATABASE
        self.server_name = server_name
        self.database = database
        self.user_name = user_name
        self.password = password

        # DEFINE Object Vars
        self.attempts = attempts
        self.delay = delay
        self.pool_size = pool_size
        self.connection = None

        self.connect()

    def __enter__(self) -> CON:
        """
        Modification for 'with' statement usage
        :return: Return DBConnection object
        """
        self.ping()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> NONE:
        """
        Modification for 'with' statement close eventS
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: Return None, only close the DB & cursor connection
        """
        pass

    def connect(self) -> NONE:
        """
        Connect to the Database
        :return: Returns the connection cursor if connection established, or else False as it failed
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.server_name,
                user=self.user_name,
                password=self.password,
                database=self.database,
            )
        except mysql.connector.Error as e:
            logging.error(e)
            raise e

    def ping(self) -> NONE:
        """
        This method is to reestablish the DB connection
        :return: None
        """
        if self.connection and self.connection.is_connected():
            self.connection.ping(reconnect=True, attempts=self.attempts, delay=self.delay)
        else:
            self.connect()
