from typing import List, Optional, Tuple, Any

from pyarrow import flight
from flightsql.api import (
    flightsql_execute,
    flightsql_get_columns,
    flightsql_get_table_names,
    flightsql_get_schema_names,
)
from flightsql.exceptions import Error, NotSupportedError

paramstyle = "pyformat"
apilevel = "2.0"

def check_closed(f):
    def g(self, *args, **kwargs):
        if self.closed:
            raise Error(f"{self.__class__.__name__} already closed")
        return f(self, *args, **kwargs)
    return g

def check_result(f):
    def g(self, *args, **kwargs):
        if self._results is None:
            raise Error('called before execute')
        return f(self, *args, **kwargs)
    return g

class Cursor():
    def __init__(self,
                 flight_client: flight.FlightClient,
                 options: Optional[flight.FlightCallOptions] = None):
        self.flight_client = flight_client
        self.options = options
        self.arraysize = 1
        self.closed = False
        self.description: Optional[List[Any]] = None
        self._results: List[Any] = []

    @check_closed
    def __iter__(self):
        return iter(self._results)

    @check_closed
    def close(self) -> None:
        self.closed = True

    @check_closed
    def execute(self, query: str, params=None) -> "Cursor":
        self.description = None
        self._results, self.description = flightsql_execute(query, self.flight_client, self.options)
        return self

    @check_closed
    def executemany(self, query: str):
        raise NotSupportedError('executemany is not supported')

    @check_result
    @check_closed
    def fetchone(self) -> Optional[Tuple[Any, ...]]:
        try:
            return self._results.pop(0)
        except IndexError:
            return None

    @check_result
    @check_closed
    def fetchmany(self, size: Optional[int] = None) -> List[Tuple[Any, ...]]:
        size = size or self.arraysize
        out = self._results[:size]
        self._results = self._results[size:]
        return out

    @check_result
    @check_closed
    def fetchall(self):
        out = self._results[:]
        self._results = []
        return out

    @check_closed
    def setinputsizes(self, sizes):
        pass

    @check_closed
    def setoutputsizes(self, sizes):
        pass

    @property
    @check_result
    @check_closed
    def rowcount(self) -> int:
        return len(self._results)

class Connection():
    def __init__(self,
                 flight_client: flight.FlightClient,
                 flight_call_options: Optional[flight.FlightCallOptions],
                 **kwargs):
        self.flight_client = flight_client
        self.options = flight_call_options
        self.closed = False
        self.cursors: List[Cursor] = []

    def __enter__(self) -> "Connection":
        return self

    def __exit__(self, *args) -> None:
        self.commit()
        self.close()

    @check_closed
    def commit(self):
        pass

    @check_closed
    def rollback(self):
        pass

    @check_closed
    def close(self) -> None:
        self.closed = True
        for cursor in self.cursors:
            cursor.close()

    @check_closed
    def cursor(self) -> Cursor:
        cursor = Cursor(self.flight_client, self.options)
        self.cursors.append(cursor)
        return cursor

    @check_closed
    def execute(self, query) -> Cursor:
        cursor = self.cursor()
        return cursor.execute(query)

    @check_closed
    def flightsql_get_columns(self, table, schema):
        return flightsql_get_columns(table, schema, self.flight_client, self.options)

    @check_closed
    def flightsql_get_table_names(self, schema):
        return flightsql_get_table_names(schema, self.flight_client, self.options)

    @check_closed
    def flightsql_get_schema_names(self):
        return flightsql_get_schema_names(self.flight_client, self.options)

def connect(*args, **kwargs) -> Connection:
    return Connection(*args, **kwargs)
