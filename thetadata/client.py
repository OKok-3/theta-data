import io
import os

import httpx
import pendulum
import polars as pl

from thetadata.options import Options

ERROR_CODES_URL = "https://www.dropbox.com/scl/fi/c1zbaq8e45djf5zb8cy26/ErrorCodes.csv?rlkey=ryepbxvk6zmtcwq3n2s3wrf0h&dl=1"


class ThetaDataClient:
    """
    Client for Theta Data API v3

    Attributes:
        - `td_terminal_url`: Theta Data Terminal URL (e.g., `http://localhost:25503`)
        - `error_codes`: Error codes DataFrame from [Theta Data API documentation](https://docs.thetadata.us/Articles/Errors-Exchanges-Conditions/Error-Codes.html)
        - `cache_dir`: Directory to cache files (default: `.cache`)
        - `request_timeout`: Request timeout in seconds
        - `max_retries`: Maximum number of retries for a request
        - `terminal_queue_size`: Maximum number of concurrent connections to the terminal (default: 16)

    Note, as far as I understand, the terminal handles the concurrent requests by itself, and users are only limited by the queue size configured for the terminal. Hence, the `terminal_queue_size` is the maximum number of concurrent requests that can be made to the terminal.
    """

    td_terminal_url: str
    request_timeout: int
    max_retries: int
    terminal_queue_size: int
    cache_dir: str

    httpx_client: httpx.Client
    error_codes: pl.DataFrame

    # API endpoint modules
    options: Options

    def __init__(
        self,
        td_terminal_url: str,
        request_timeout: int = 30,
        max_retries: int = 3,
        terminal_queue_size: int = 16,
        cache_dir: str = ".cache",
    ):
        self.td_terminal_url = f"{td_terminal_url.rstrip('/')}/v3"
        self.request_timeout = request_timeout
        self.max_retries = max_retries
        self.terminal_queue_size = terminal_queue_size
        self.cache_dir = cache_dir

        # Initialize the client
        self.httpx_client = httpx.Client(
            base_url=self.td_terminal_url,
            timeout=self.request_timeout,
            http2=True,
            limits=httpx.Limits(max_connections=self.terminal_queue_size),
        )

        # Initialize necessary files and directories
        os.makedirs(self.cache_dir, exist_ok=True)
        self.error_codes = self._get_error_codes()

        # Test the connection to the Theta Data API
        self._test_connection()

        # Initialize API endpoint modules
        self.options = Options(self)

        self._print_init_info()

    def handle_http_error(self, response: httpx.Response) -> None:
        """Handle HTTP errors from Theta Data API

        Args:
            response: The HTTP response object.

        Raises:
            httpx.HTTPStatusError: If the response status code is not 200.
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            error_name = self.error_codes.filter(pl.col("HttpCode") == response.status_code).select("ErrorName").item()
            error_description = self.error_codes.filter(pl.col("HttpCode") == response.status_code).select("Description").item()

            raise httpx.HTTPStatusError(
                f"HTTP {response.status_code} ({error_name}): {error_description}. See https://docs.thetadata.us/Articles/Errors-Exchanges-Conditions/Error-Codes.html for more information.",
                request=response.request,
                response=response,
            ) from e

    def _get_error_codes(self) -> pl.DataFrame:
        # TODO: consider converting this into a dictionary instead
        """Get error codes from Theta Data API documentation"""
        error_codes_cache_path = f"{self.cache_dir}/error_codes.parquet"

        # Check if cache exists and is fresh (less than 30 days old)
        if os.path.exists(error_codes_cache_path):
            mod_time = os.path.getmtime(error_codes_cache_path)
            if pendulum.from_timestamp(mod_time) > pendulum.now().subtract(days=30):
                return pl.read_parquet(error_codes_cache_path)

        # Download and cache if missing or stale
        response = httpx.get(ERROR_CODES_URL, follow_redirects=True)
        response.raise_for_status()

        error_codes = pl.read_csv(io.StringIO(response.text), truncate_ragged_lines=True)

        # Remove all the trailing and leading whitespace
        error_codes.columns = [col.strip() for col in error_codes.columns]
        error_codes = error_codes.with_columns(pl.col(pl.String).exclude("HttpCode").str.strip_chars())

        os.makedirs(self.cache_dir, exist_ok=True)
        error_codes.write_parquet(error_codes_cache_path)

        return error_codes

    def _test_connection(self) -> None:
        """Test the connection to the Theta Data API"""
        date = pendulum.now().format("YYYY-MM-DD")

        response = self.httpx_client.get("/calendar/on_date", params={"date": date})
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ConnectionError("Failed to connect to the Theta Data terminal. Please check your terminal URL and try again.") from e

    def _print_init_info(self) -> None:
        # TODO: Add error code cache info (date it was downloaded, and whether it was renewed)
        """Print initialization information. This is implemented for debugging purposes, especially when used in notebooks."""
        info = {
            "Setting": [
                "Theta Data Terminal URL",
                "Request timeout",
                "Max retries",
                "Max concurrent connections",
                "Cache directory",
            ],
            "Value": [
                self.td_terminal_url,
                f"{self.request_timeout} seconds",
                str(self.max_retries),
                str(self.terminal_queue_size),
                os.path.abspath(self.cache_dir),
            ],
        }

        with pl.Config(
            tbl_hide_dataframe_shape=True,
            fmt_str_lengths=1000,
            tbl_formatting="UTF8_FULL",
        ):
            print(pl.DataFrame(info))
