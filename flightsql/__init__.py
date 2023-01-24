from flightsql.client import FlightSQLCallOptions, FlightSQLClient
from flightsql.dbapi import apilevel, connect, paramstyle
from flightsql.exceptions import (
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Warning,
)

__version__ = "0.1.0"

__all__ = [
    "connect",
    "apilevel",
    "paramstyle",
    "DataError",
    "DatabaseError",
    "Error",
    "IntegrityError",
    "InterfaceError",
    "InternalError",
    "NotSupportedError",
    "OperationalError",
    "ProgrammingError",
    "Warning",
    "FlightSQLClient",
    "FlightSQLCallOptions",
]
