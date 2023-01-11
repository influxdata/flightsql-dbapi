from typing import Any, Dict, Optional, Tuple
from pyarrow import flight

def create_client(host: str = "localhost",
                  port: int = 443,
                  user: Optional[str] = None,
                  password: Optional[str] = None,
                  token: Optional[str] = None,
                  insecure: Optional[bool] = None,
                  disable_server_verification: Optional[bool] = None,
                  metadata: Optional[Dict[str, str]] = None,
                  features: Optional[Dict[str, str]] = None,
                  **kwargs: Any) -> Tuple[flight.FlightClient,
                                          flight.FlightCallOptions,
                                          Dict[str, str]]:

    protocol = 'tls'
    client_args = {}
    if insecure:
        protocol = 'tcp'
    elif disable_server_verification:
        client_args['disable_server_verification'] = True

    url = f"grpc+{protocol}://{host}:{port}"
    client = flight.FlightClient(url, **client_args)

    headers = []
    if user or password:
        headers.append(client.authenticate_basic_token(user, password))
    else:
        headers.append((b'authorization', f"Bearer {token}".encode('utf-8')))

    if metadata:
        for k, v in metadata.items():
            headers.append((k.encode('utf-8'), v.encode('utf-8')))

    if features is None:
        features = {}

    return client, flight.FlightCallOptions(headers=headers), features
