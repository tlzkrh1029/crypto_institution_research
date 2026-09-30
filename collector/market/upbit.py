"""Upbit Open API (quotation endpoints, no key needed).

Terms: Upbit Open API 이용약관 (effective 2024-10-30), checked 2026-09-30.
Rate limit: at most 10 requests per second per IP for each endpoint group;
429 means too many requests and repeated 429s lead to a temporary block (418).
"""

from __future__ import annotations

from datetime import datetime, timezone

import requests

from ..fetch import FetchError
from .base import Candle, RateLimitedJSON, Ticker

BASE = "https://api.upbit.com/v1"
MIN_REQUEST_GAP_SEC = 0.2    # 5 requests/second, half the published limit
MAX_CANDLES = 200


class UpbitClient:
    name = "upbit"
    pages_backward = True

    def __init__(self, user_agent: str, session: requests.Session | None = None, **kwargs):
        self.http = RateLimitedJSON(user_agent, MIN_REQUEST_GAP_SEC, session, **kwargs)

    def _get(self, path: str, params: dict) -> list:
        data = self.http.get(f"{BASE}{path}", params)
        if not isinstance(data, list):
            raise FetchError(f"unexpected response: {str(data)[:200]}")
        return data

    def market_id(self, symbol: str, quote: str) -> str:
        return f"{quote}-{symbol}"

    def markets(self) -> set[str]:
        return {m["market"] for m in self._get("/market/all", {})}

    def tickers(self, market_ids: list[str]) -> list[Ticker]:
        data = self._get("/ticker", {"markets": ",".join(market_ids)})
        return [Ticker(
            market=row["market"],
            price=float(row["trade_price"]),
            acc_trade_value_24h=row.get("acc_trade_price_24h"),
            ts=datetime.fromtimestamp(row["timestamp"] / 1000, tz=timezone.utc),
        ) for row in data]

    def hourly_candles(self, market_id: str, to: datetime,
                       count: int = MAX_CANDLES) -> list[Candle]:
        """Up to `count` 60-minute candles that start before `to`, newest first.

        Upbit creates a candle only for hours with trades, so gaps are possible.
        """
        data = self._get("/candles/minutes/60", {
            "market": market_id,
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
