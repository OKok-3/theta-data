import io
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from thetadata.client import ThetaDataClient


class OptionsList:
    """Endpoint module for the options list endpoint"""

    def __init__(self, client: ThetaDataClient) -> None:
        self.client = client
        self.httpx_client = client.httpx_client

    def symbols(self, format: str = "ndjson") -> io.BytesIO:
        pass

    def dates(self, symbol: str, expiration: str, strike: float, right: str, format: str = "ndjson") -> io.BytesIO:
        pass

    def expirations(self, symbol: str, format: str = "ndjson") -> io.BytesIO:
        pass

    def strikes(self, symbol: str, expiration: str, format: str = "ndjson") -> io.BytesIO:
        pass

    def contracts(self, symbol: str, date: str, format: str = "ndjson") -> io.BytesIO:
        pass
