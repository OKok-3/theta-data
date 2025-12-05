from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from thetadata.client import ThetaDataClient

from thetadata.options.list import OptionsList


class Options:
    """Endpoint module for the options endpoint.

    This module contains all the endpoints for the options endpoint.

    Attributes:
        - `client`: The `ThetaDataClient` instance that this module belongs to.
        - `httpx_client`: The `httpx` client instance that this module uses to make requests to the Theta Data API.

    Available endpoints:
        - `list`: Lists all symbols, dates, expirations, strikes, and contracts for options.
    """

    client: ThetaDataClient
    httpx_client: httpx.Client

    def __init__(self, client: ThetaDataClient) -> None:
        self.client = client
        self.httpx_client = client.httpx_client

        # Initialize endpoint classes
        self.list = OptionsList(self.client)
