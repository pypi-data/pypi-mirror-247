import mysql.connector.pooling
import logging
from vvecon.rest_api.utils.Types import NONE, CON


class DBConnection:
    def __init__(self, server_name: str = "", database: str = "", user_name: str = "", password: str = "", attempts: int = 2, delay: int = 100, pool_size: int = 32) -> NONE:
        """
        Setup all the required variables in order to keep the DB connection
        """

        # CONFIGURE DATABASE
        self.server_name = server_name
        self.database = database
        self.user_name = user_name
        self.password = password

        # DEFINE Object Vars
        self.pool_size = pool_size
        self.attempts = attempts
        self.delay = delay
        self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="pool",
            pool_size=self.pool_size,
            host=self.server_name,
            user=self.user_name,
            password=self.password,
            database=self.database,
        )

    def __enter__(self) -> object:
        """
        Modification for 'with' statement usage
        :return: Return DBConnection object
        """
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb) -> NONE:
        """
        Modification for 'with' statement close eventS
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: Return None, only close the DB & cursor connection
        """
        pass

    def connect(self) -> CON:
        """
        Connect to the Database
        :return: Returns the db cursor if connection established, or else False as it failed
        """
        try:
            return self.connection_pool.get_connection()
        except mysql.connector.Error as e:
            logging.error(e)
            raise e
