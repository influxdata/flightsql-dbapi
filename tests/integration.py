import os

from flightsql.client import FlightSQLClient

disabled_message = "INTEGRATION not set to 1. Skipping."


def is_disabled():
    return not (bool(os.getenv("INTEGRATION")) or False)


def host_port():
    host = os.getenv("FLIGHTSQL_SERVER_HOST", default="127.0.0.1")
    port = int(os.getenv("FLIGHTSQL_SERVER_PORT", default=3000))
    return host, port


def new_client(features={}):
    host, port = host_port()
    return FlightSQLClient(host=host, port=port, insecure=True, features=features)
