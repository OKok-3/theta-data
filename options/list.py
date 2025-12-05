"""Scrape OHLC data from Theta Data"""

import io
import os

import httpx
from dotenv import load_dotenv

load_dotenv()
TT_HOST = os.environ.get("TT_HOST")


def get_all_symbols(client: httpx.Client, format: str) -> io.BytesIO:
    """Get all symbols from Theta Data"""
    url = f"{TT_HOST}/option/list/symbols"
    params = {"format": format}

    with client.stream("GET", url, params=params) as response:
        response.raise_for_status()
        return io.BytesIO(response.read())


def get_expirations(client: httpx.Client, symbol: str, format: str) -> io.BytesIO:
    """Get all expirations for a symbol using streaming"""
    url = f"{TT_HOST}/option/list/expirations"
    params = {"format": format, "symbol": symbol}

    with client.stream("GET", url, params=params) as response:
        response.raise_for_status()
        return io.BytesIO(response.read())


def get_strikes(client: httpx.Client, symbol: str, expiration: str, format: str) -> io.BytesIO:
    """Get all strikes for a symbol and expiration"""
    url = f"{TT_HOST}/option/list/strikes"
    params = {"format": format, "symbol": symbol, "expiration": expiration}

    with client.stream("GET", url, params=params) as response:
        response.raise_for_status()
        return io.BytesIO(response.read())


def get_dates(client: httpx.Client, symbol: str, expiration: str, strike: str, right: str, format: str, request_type: str) -> io.BytesIO:
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
        return io.BytesIO(response.read())
