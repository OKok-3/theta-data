from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from thetadata.client import ThetaDataClient


class OptionsList:
    """Endpoint module for the options list endpoint"""

    def __init__(self, client: ThetaDataClient) -> None:
        self.client = client
        self.httpx_client = client.httpx_client

    def symbols(self, format: str = "ndjson") -> httpx.Response:
        """Get list of symbols from Theta Data API

        Args:
            format: Format of the response (default: "ndjson")

        Returns:
            httpx.Response: The HTTP response object.
        """
        path = "/option/list/symbols"
        params = {"format": format}

        response = self.httpx_client.get(path, params=params)
        self.client.handle_http_error(response)

        return response

    def dates(self, symbol: str, expiration: str, strike: str | float, right: str, request_type: str, format: str = "ndjson") -> httpx.Response:
        """
        Get list of dates from Theta Data API

        Args:
            symbol: Symbol of the underlying asset
            expiration: Expiration date of the option
            strike: Strike price of the option (e.g., "100.00", "$100.00", or "*" for all strikes)
            right: Right of the option
            request_type: Type of request ("trade" or "quote")
            format: Format of the response (default: "ndjson")

        Returns:
            httpx.Response: The HTTP response object.
        """
        path = f"/option/list/dates/{request_type}"
        params = {
            "symbol": symbol,
            "expiration": expiration,
            "strike": strike,
            "right": right,
            "format": format,
        }

        response = self.httpx_client.get(path, params=params)
        self.client.handle_http_error(response)

        return response

    def expirations(self, symbol: str, format: str = "ndjson") -> httpx.Response:
        """
        Get list of expirations from Theta Data API

        Args:
            symbol: Symbol of the underlying asset
            format: Format of the response (default: "ndjson")

        Returns:
            httpx.Response: The HTTP response object.
        """
        path = "/option/list/expirations"
        params = {"symbol": symbol, "format": format}

        response = self.httpx_client.get(path, params=params)
        self.client.handle_http_error(response)
        return response

    def strikes(self, symbol: str, expiration: str, format: str = "ndjson") -> httpx.Response:
        """
        Get list of strikes from Theta Data API

        Args:
            symbol: Symbol of the underlying asset
            expiration: Expiration date of the option
            format: Format of the response (default: "ndjson")

        Returns:
            httpx.Response: The HTTP response object.
        """
        path = "/option/list/strikes"
        params = {"symbol": symbol, "expiration": expiration, "format": format}

        response = self.httpx_client.get(path, params=params)
        self.client.handle_http_error(response)
        return response

    def contracts(self, symbol: str, date: str, format: str = "ndjson") -> httpx.Response:
        pass
