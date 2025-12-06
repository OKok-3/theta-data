from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from thetadata.client import ThetaDataClient


class OptionsHistory:
    """
    This module contains all the endpoints for the options history endpoint. Consult the [official documentation](https://docs.thetadata.us) for more information.

    Attributes:
        - `client`: The `ThetaDataClient` instance that this module belongs to.
        - `httpx_client`: The `httpx` client instance that this module uses to make requests to the Theta Data API.

    Methods:
        # TODO: add methods
    """

    client: ThetaDataClient
    httpx_client: httpx.Client

    def __init__(self, client: ThetaDataClient) -> None:
        self.client = client
        self.httpx_client = client.httpx_client
