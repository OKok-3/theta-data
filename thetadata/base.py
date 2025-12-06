from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from thetadata.client import ThetaDataClient


class Endpoint:
    """Base class for all endpoint classes.

    Attributes:
        - `client`: The `ThetaDataClient` instance that this class belongs to.
        - `httpx_client`: The `httpx` client instance that this class uses to make requests to the Theta Data API.
    """

    client: ThetaDataClient
    httpx_client: httpx.Client

    def __init__(self, client: ThetaDataClient) -> None:
        self.client = client
        self.httpx_client = client.httpx_client
