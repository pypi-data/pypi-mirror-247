from vvecon.rest_api.connections import MySQLDBConnection
from vvecon.rest_api.connections import MySQLDBSingleConnection
from vvecon.rest_api.utils.Types import CON

__all__ = ("MySQLDBConnection", "MySQLDBSingleConnection", "get_connection")


def get_connection(server_name: str = "", database: str = "", user_name: str = "", password: str = "",
                   system: str = "mysql", method: str = "single", attempts: int = 2, delay: int = 100,
                   pool_size: int = 32) -> CON:
    connections = {
        "mysql": {
            "multi": MySQLDBConnection,
            "single": MySQLDBSingleConnection
        }
    }

    if system in connections:
        if method in connections[system]:
            return connections[system][method].DBConnection(server_name, database, user_name, password, attempts, delay,
                                                            pool_size)
        else:
            raise AttributeError("Invalid method")
    else:
        raise AttributeError("Invalid system")
