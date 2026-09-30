"""Upbit Open API (quotation endpoints, no key needed).

Terms: Upbit Open API 이용약관 (effective 2024-10-30), checked 2026-09-30.
Rate limit: at most 10 requests per second per IP for each endpoint group;
429 means too many requests and repeated 429s lead to a temporary block (418).
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone

import requests

from ..fetch import FetchError

BASE = "https://api.upbit.com/v1"
MIN_REQUEST_GAP_SEC = 0.2    # 5 requests/second, half the published limit
MAX_CANDLES = 200


@dataclass(frozen=True)
class Ticker:
    market: str
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


class UpbitClient:
    def __init__(self, user_agent: str, session: requests.Session | None = None,
                 sleep=time.sleep, monotonic=time.monotonic):
        self.user_agent = user_agent
        self.session = session or requests.Session()
        self._sleep = sleep
        self._monotonic = monotonic
        self._last_request = 0.0

    def _get(self, path: str, params: dict) -> list:
        wait = MIN_REQUEST_GAP_SEC - (self._monotonic() - self._last_request)
        if wait > 0:
            self._sleep(wait)
        self._last_request = self._monotonic()
        try:
            resp = self.session.get(f"{BASE}{path}", params=params, timeout=20,
                                    headers={"User-Agent": self.user_agent,
                                             "Accept": "application/json"})
        except requests.RequestException as exc:
            raise FetchError(f"{type(exc).__name__}: {exc}") from exc
        if resp.status_code != 200:
            raise FetchError(f"HTTP {resp.status_code}", resp.status_code)
        try:
            data = resp.json()
        except (ValueError, json.JSONDecodeError) as exc:
            raise FetchError(f"bad JSON: {exc}") from exc
        if not isinstance(data, list):
            raise FetchError(f"unexpected response: {str(data)[:200]}")
        return data

    def markets(self) -> set[str]:
        return {m["market"] for m in self._get("/market/all", {})}

    def tickers(self, markets: list[str]) -> list[Ticker]:
        data = self._get("/ticker", {"markets": ",".join(markets)})
        return [Ticker(
            market=row["market"],
            price=float(row["trade_price"]),
            acc_trade_value_24h=row.get("acc_trade_price_24h"),
            ts=datetime.fromtimestamp(row["timestamp"] / 1000, tz=timezone.utc),
        ) for row in data]

    def hourly_candles(self, market: str, to: datetime, count: int = MAX_CANDLES) -> list[Candle]:
        """Up to `count` 60-minute candles that start before `to`, newest first.

        Upbit creates a candle only for hours with trades, so gaps are possible.
        """
        data = self._get("/candles/minutes/60", {
            "market": market,
            "to": to.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "count": min(count, MAX_CANDLES),
        })
        return [Candle(
            market=row["market"],
            start_at=datetime.fromisoformat(row["candle_date_time_utc"]).replace(
                tzinfo=timezone.utc),
            open=float(row["opening_price"]),
            high=float(row["high_price"]),
            low=float(row["low_price"]),
            close=float(row["trade_price"]),
            volume=row.get("candle_acc_trade_volume"),
        ) for row in data]
