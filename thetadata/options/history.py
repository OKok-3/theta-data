from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from thetadata.client import ThetaDataClient


class OptionsHistory:
    """Endpoint module for the options history endpoint.

    This module contains all the endpoints for the options history endpoint.
    """

    client: ThetaDataClient
    httpx_client: httpx.Client

    def __init__(self, client: ThetaDataClient) -> None:
        self.client = client
        self.httpx_client = client.httpx_client
