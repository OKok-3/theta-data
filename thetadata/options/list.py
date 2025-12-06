import httpx

from thetadata.base import Endpoint


class OptionsList(Endpoint):
    """
    This class contains all the endpoints for the options list endpoint. Consult the [official documentation](https://docs.thetadata.us) for more information.

    Attributes:
        - `client`: The `ThetaDataClient` instance that this class belongs to.
        - `httpx_client`: The `httpx` client instance that this class uses to make requests to the Theta Data API.

    Methods:
        - `symbols`: Lists all symbols that are available for options.
        - `dates`: Lists all dates of data that are available for an option with a given symbol, request type, and expiration.
        - `expirations`: Lists all dates of expirations that are available for an option with a given symbol.
        - `strikes`: Lists all strikes that are available for an option with a given symbol and expiration date.
        - `contracts`: Lists all contracts that were traded or quoted on a particular date.
    """

    def symbols(self, format: str = "ndjson") -> httpx.Response:
        """
        Lists all symbols for options.

        A `symbol` can be defined as a unique identifier for a stock / underlying asset. Common terms also include: root, ticker, and underlying. This endpoint returns all traded symbols for options. This endpoint is updated overnight.

        Args:
            - `format`: Format of the response (optional, default: `"ndjson"`)

        Returns:
            - `httpx.Response`: The `httpx` response object.
        """
        path = "/option/list/symbols"
        params = {"format": format}

        response = self.httpx_client.get(path, params=params)
        self.client.handle_http_error(response)

        return response

    def dates(
        self,
        symbol: str,
        expiration: str,
        request_type: str,
        strike: str = "*",
        right: str = "both",
        format: str = "ndjson",
    ) -> httpx.Response:
        """
        Lists all dates of data that are available for an option with a given symbol, request type, and expiration.

        This endpoint is updated overnight.

        Args:
            - `symbol`: Symbol of the underlying asset
            - `expiration`: Expiration date of the option
            - `strike`: Strike price of the option (optional, default: `"*"`. E.g., `"100.00"`, `"$100.00"`, or `"*"` for all strikes)
            - `right`: Right of the option (optional, default: `"both"`)
            - `request_type`: Type of request (`"trade"` or `"quote"`)
            - `format`: Format of the response (optional, default: `"ndjson"`)

        Returns:
            - `httpx.Response`: The `httpx` response object.
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
        Lists all dates of expirations that are available for an option with a given symbol.

        This endpoint is updated overnight.

        Args:
            - `symbol`: Symbol of the underlying asset
            - `format`: Format of the response (optional, default: `"ndjson"`)

        Returns:
            - `httpx.Response`: The `httpx` response object.
        """
        path = "/option/list/expirations"
        params = {"symbol": symbol, "format": format}

        response = self.httpx_client.get(path, params=params)
        self.client.handle_http_error(response)
        return response

    def strikes(self, symbol: str, expiration: str, format: str = "ndjson") -> httpx.Response:
        """
        Lists all strikes that are available for an option with a given symbol and expiration date.

        This endpoint is updated overnight.

        Args:
            - `symbol`: Symbol of the underlying asset
            - `expiration`: Expiration date of the option
            - `format`: Format of the response (optional, default: `"ndjson"`)

        Returns:
            - `httpx.Response`: The `httpx` response object.
        """
        path = "/option/list/strikes"
        params = {"symbol": symbol, "expiration": expiration, "format": format}

        response = self.httpx_client.get(path, params=params)
        self.client.handle_http_error(response)
        return response

    def contracts(self, date: str, request_type: str, symbol: str = None, format: str = "ndjson") -> httpx.Response:
        """
        Lists all contracts that were traded or quoted on a particular date.

        If the `symbol` parameter is specified, the returned contracts will be filtered to match the symbol.
        Multiple symbols can be specified by separating them with commas such as `symbol=AAPL,SPY,AMD`
        This endpoint is updated real-time.

        Args:
            - `symbol`: Symbol of the underlying asset (optional)
            - `date`: Date of the contract
            - `request_type`: Type of request (`"trade"` or `"quote"`)
            - `format`: Format of the response (optional, default: `"ndjson"`)

        Returns:
            - `httpx.Response`: The `httpx` response object.
        """
        path = f"/option/list/contracts/{request_type}"
        params = {
            "symbol": symbol,
            "date": date,
            "format": format,
        }

        response = self.httpx_client.get(path, params=params)
        self.client.handle_http_error(response)
        return response
