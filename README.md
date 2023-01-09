This library provides a [DB API 2](https://peps.python.org/pep-0249/) interface
and [SQLAlchemy](https://www.sqlalchemy.org) Dialect for [Flight
SQL](https://arrow.apache.org/docs/format/FlightSql.html).

Initially, this library aims to ease the process of connecting to Flight SQL
APIs in [Apache Superset](https://superset.apache.org). The SQLAlchemy Dialect
is read-only for now, but should expand its capabilities as time progresses.

## Usage

### DB API 2 Interface ([PEP-249](https://peps.python.org/pep-0249))

```python3
from flightsql.dbapi import connect
from flightsql.flight import create_client

conn = connect(*create_client(host='upstream.server.dev'))
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

engine = create_engine("readonly+flightsql://john:appleseeds@upstream.server.dev:443")
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

### Authentication

Both [Basic and Bearer Authentication](https://arrow.apache.org/docs/format/Flight.html#authentication) are supported. 

To authenticate using Basic Authentication, supply a DSN as follows:

```
readonly+flightsql://user:password@host:443
```

A handshake will be performed with the upstream server to obtain a Bearer token.
That token will be used for the remainder of the engine's lifetype.

To authenticate using Bearer Authentication directly, supply a `token` query parameter
instead:

```
readonly+flightsql://host:443?token=TOKEN
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
