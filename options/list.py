"""Scrape OHLC data from Theta Data"""

import io
import os

import httpx
import polars as pl
from dotenv import load_dotenv

load_dotenv()

TT_HOST = os.environ.get("TT_HOST")


def get_all_symbols(client: httpx.Client, format: str) -> pl.DataFrame:
    """Get all symbols from Theta Data"""
    url = f"{TT_HOST}/option/list/symbols"
    params = {"format": format}

    response = client.get(url, params=params)
    response.raise_for_status()

    return pl.read_ndjson(io.BytesIO(response.content))


def get_expirations(client: httpx.Client, symbol: str, format: str) -> pl.DataFrame:
    """Get all expirations for a symbol using streaming"""
    url = f"{TT_HOST}/option/list/expirations"
    params = {"format": format, "symbol": symbol}

    with client.stream("GET", url, params=params) as response:
        response.raise_for_status()
        return pl.read_ndjson(io.BytesIO(response.read()))


def get_strikes(client: httpx.Client, symbol: str, expiration: str, format: str) -> pl.DataFrame:
    """Get all strikes for a symbol and expiration"""
    url = f"{TT_HOST}/option/list/strikes"
    params = {"format": format, "symbol": symbol, "expiration": expiration}

    with client.stream("GET", url, params=params) as response:
        response.raise_for_status()
        return pl.read_ndjson(io.BytesIO(response.read()))


def get_dates(client: httpx.Client, symbol: str, expiration: str, strike: str, right: str, format: str, request_type: str) -> pl.DataFrame:
    """Get all dates for a symbol and expiration"""
    url = f"{TT_HOST}/option/list/dates/{request_type}"
    params = {
        "format": format,
        "symbol": symbol,
        "expiration": expiration,
        "strike": strike,
        "right": right,
    }

    with client.stream("GET", url, params=params) as response:
        response.raise_for_status()
        return pl.read_ndjson(io.BytesIO(response.read()))


if __name__ == "__main__":
    client = httpx.Client()
    print(get_dates(client, "AAPL", "2025-12-05", "285", "C", "ndjson", "trade"))
