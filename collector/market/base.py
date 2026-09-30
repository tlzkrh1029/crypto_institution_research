"""Shared types for market-data venues."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

import requests

from ..fetch import FetchError


@dataclass(frozen=True)
class Ticker:
    market: str           # venue-specific market id, e.g. KRW-HBAR or QNTUSD
    price: float
    acc_trade_value_24h: float | None
    ts: datetime


@dataclass(frozen=True)
class Candle:
    market: str
    start_at: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float | None


class VenueClient(Protocol):
    name: str
    pages_backward: bool   # True if hourly_candles honours `to` (older pages)

    def market_id(self, symbol: str, quote: str) -> str: ...
    def markets(self) -> set[str]: ...
    def tickers(self, market_ids: list[str]) -> list[Ticker]: ...
    def hourly_candles(self, market_id: str, to: datetime) -> list[Candle]: ...


class RateLimitedJSON:
    """GET JSON with a descriptive User-Agent and a minimum gap between requests."""

    def __init__(self, user_agent: str, min_gap_sec: float,
                 session: requests.Session | None = None, sleep=time.sleep,
                 monotonic=time.monotonic):
        self.user_agent = user_agent
        self.min_gap_sec = min_gap_sec
        self.session = session or requests.Session()
        self._sleep = sleep
        self._monotonic = monotonic
        self._last = float("-inf")

    def get(self, url: str, params: dict):
        wait = self.min_gap_sec - (self._monotonic() - self._last)
        if wait > 0:
            self._sleep(wait)
        self._last = self._monotonic()
        try:
            resp = self.session.get(url, params=params, timeout=20,
                                    headers={"User-Agent": self.user_agent,
                                             "Accept": "application/json"})
        except requests.RequestException as exc:
            raise FetchError(f"{type(exc).__name__}: {exc}") from exc
        if resp.status_code != 200:
            raise FetchError(f"HTTP {resp.status_code}", resp.status_code)
        try:
            return resp.json()
        except (ValueError, json.JSONDecodeError) as exc:
            raise FetchError(f"bad JSON: {exc}") from exc
