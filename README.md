:warning: This library is experimental and under active development. The APIs it
provides could change at any time so use at your own risk.

## Overview

This library provides a [DB API 2](https://peps.python.org/pep-0249/) interface
and [SQLAlchemy](https://www.sqlalchemy.org) Dialect for [Flight
SQL](https://arrow.apache.org/docs/format/FlightSql.html).

Initially, this library aims to ease the process of connecting to Flight SQL
APIs in [Apache Superset](https://superset.apache.org).

The primary SQLAlchemy Dialect provided by `flightsql-dbapi` targets the
[DataFusion](https://arrow.apache.org/datafusion) SQL execution engine. However,
there extension points to create custom dialects using Flight SQL as a transport
layer and for metadata discovery.

## Installation

```shell
$ pip install flightsql-dbapi
```

## Usage

### DB API 2 Interface ([PEP-249](https://peps.python.org/pep-0249))

```python3
from flightsql import connect, FlightSQLClient

client = FlightSQLCLient(host='upstream.server.dev')
conn = connect(client)
cursor = conn.cursor()
cursor.execute('select * from runs limit 10')
print("columns:", cursor.description)
print("rows:", [r for r in cursor])
```

### SQLAlchemy

```python3
import flightsql.sqlalchemy
from sqlalchemy import func, select
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, Table

engine = create_engine("datafusion+flightsql://john:appleseeds@upstream.server.dev:443")
runs = Table("runs", MetaData(bind=engine), autoload=True)
count = select([func.count("*")], from_obj=runs).scalar()
print("runs count:" count)
print("columns:", [(r.name, r.type) for r in runs.columns])

# Reflection
metadata = MetaData(schema="iox")
metadata.reflect(bind=engine)
print("tables:", [table for table in metadata.sorted_tables])
```

### Custom Dialects

If your database of choice can't make use of the Dialects provided by this
library directly, you can extend `flightsql.sqlalchemy.FlightSQLDialect` as a
starting point for your own custom Dialect.

```python3
from flightsql.sqlalchemy import FlightSQLDialect
from sqlalchemy.dialects import registry

class CustomDialect(FlightSQLDialect):
    name = "custom"
    paramstyle = 'named'

    # For more information about what's available to override, visit:
    # https://docs.sqlalchemy.org/en/14/core/internals.html#sqlalchemy.engine.default.DefaultDialect

registry.register("custom.flightsql", "path.to.your.module", "CustomDialect")
```

DB API 2 Connection creation is provided by `FlightSQLDialect`.

The core reflection APIs of `get_columns`, `get_table_names` and
`get_schema_names` are implemented in terms of Flight SQL API calls so you
shouldn't have to override those unless you have very specific needs.

### Directly with `flightsql.FlightSQLClient`

```python3
from flightsql import FlightSQLClient


client = FlightSQLClient(host='upstream.server.dev',
                         port=443,
                         token='rosebud-motel-bearer-token')
info = client.execute("select * from runs limit 10")
reader = client.do_get(info.endpoints[0].ticket)

data_frame = reader.read_all().to_pandas()
```

### Authentication

Both [Basic and Bearer Authentication](https://arrow.apache.org/docs/format/Flight.html#authentication) are supported.

To authenticate using Basic Authentication, supply a DSN as follows:

```
datafusion+flightsql://user:password@host:443
```

A handshake will be performed with the upstream server to obtain a Bearer token.
That token will be used for the remainder of the engine's lifetype.

To authenticate using Bearer Authentication directly, supply a `token` query parameter
instead:

```
datafusion+flightsql://host:443?token=TOKEN
```

The token will be placed in an appropriate `Authentication: Bearer ...` HTTP header.

### Additional Query Parameters

| Name | Description | Default |
| ---- | ----------- | ------- |
| `insecure` | Connect without SSL/TLS (h2c) | `false` |
| `disable_server_verification` | Disable certificate verification of the upstream server | `false` |
| `token` | Bearer token to use instead of Basic Auth | empty |

Any query parameters *not* specified in the above table will be sent to the
upstream server as gRPC metadata.
