from typing import Union, Any
from mysql.connector.pooling import MySQLConnection
from mysql.connector.cursor import MySQLCursor


# unions & data types
BOOL = bool
NONE: None = None
BONE = Union[bool, None]
ALL_ = Union[bool, int, str, float, None]
ANY_ = Union[bool, int, str, float, None, list, dict]
ANY = Any
LIST = Union[bool, list]
DICT = Union[bool, dict]
OBJ_ = object
OBJET = Union[object, type]
CURSOR = MySQLCursor
CON = MySQLConnection


# This function will validate weather the argument is None, Empty, Or Str
def str__(value: str) -> str:
    if value is None:
        raise ValueError("Value cannot be None")
    if not isinstance(value, str):
        raise ValueError("Invalid argument")
    if not value.strip():
        raise ValueError("Value cannot be empty or whitespace")
    return str(value)


# This function will validate weather the argument is None or Int
def int__(value: int) -> int:
    if value is None:
        raise ValueError("Value cannot be None")
    if not isinstance(value, int):
        raise ValueError("Invalid argument")
    return int(value)


# This function will validate weather the argument is None or Float
def float__(value: float) -> float:
    if value is None:
        raise ValueError("Value cannot be None")
    if not isinstance(value, float):
        raise ValueError("Invalid argument")
    return float(value)
