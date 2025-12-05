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
        """Get list of symbols from Theta Data API

        Args:
            format: Format of the response (default: "ndjson")

        Returns:
            io.BytesIO: A bytes buffer containing the response.
        """
        path = "/option/list/symbols"
        params = {"format": format}

        response = self.httpx_client.get(path, params=params)

        response.raise_for_status()
        return io.BytesIO(response.read())

    def dates(self, symbol: str, expiration: str, strike: float, right: str, format: str = "ndjson") -> io.BytesIO:
        pass

    def expirations(self, symbol: str, format: str = "ndjson") -> io.BytesIO:
        """
        Get list of expirations from Theta Data API

        Args:
            symbol: Symbol of the underlying asset
            format: Format of the response (default: "ndjson")

        Returns:
            io.BytesIO: A bytes buffer containing the response.
        """
        path = "/option/list/expirations"
        params = {"symbol": symbol, "format": format}

        response = self.httpx_client.get(path, params=params)
        response.raise_for_status()
        return io.BytesIO(response.read())

    def strikes(self, symbol: str, expiration: str, format: str = "ndjson") -> io.BytesIO:
        """
        Get list of strikes from Theta Data API

        Args:
            symbol: Symbol of the underlying asset
            expiration: Expiration date of the option
            format: Format of the response (default: "ndjson")

        Returns:
            io.BytesIO: A bytes buffer containing the response.
        """
        path = "/option/list/strikes"
        params = {"symbol": symbol, "expiration": expiration, "format": format}

        response = self.httpx_client.get(path, params=params)
        response.raise_for_status()
        return io.BytesIO(response.read())

    def contracts(self, symbol: str, date: str, format: str = "ndjson") -> io.BytesIO:
        pass
