"""Kraken public REST API (no key needed). Used for QNT, which Upbit does not list
(docs/decisions.md D-012).

Terms: the API notice allows personal use of the public endpoints and asks
for permission for non-personal commercial use; checked 2026-09-30.
Kraken publishes no numeric public limit; its support site says one call per
second or less stays within the limits.
OHLC returns only the most recent 720 candles (30 days of hourly candles).
"""

from __future__ import annotations

from datetime import datetime, timezone

import requests

from ..fetch import FetchError
from .base import Candle, RateLimitedJSON, Ticker

BASE = "https://api.kraken.com/0/public"
MIN_REQUEST_GAP_SEC = 1.1
ALIASES = {"BTC": "XBT"}


class KrakenClient:
    name = "kraken"
    pages_backward = False

    def __init__(self, user_agent: str, session: requests.Session | None = None, **kwargs):
        self.http = RateLimitedJSON(user_agent, MIN_REQUEST_GAP_SEC, session, **kwargs)
        self._key_to_alt: dict[str, str] = {}

    def _get(self, path: str, params: dict) -> dict:
        data = self.http.get(f"{BASE}{path}", params)
        if not isinstance(data, dict) or data.get("error"):
            raise FetchError(f"kraken error: {data.get('error') if isinstance(data, dict) else data}")
        return data["result"]

    def market_id(self, symbol: str, quote: str) -> str:
        return f"{ALIASES.get(symbol, symbol)}{quote}"

    def markets(self) -> set[str]:
        pairs = self._get("/AssetPairs", {})
        self._key_to_alt = {key: info["altname"] for key, info in pairs.items()}
        return set(self._key_to_alt.values())

    def _alt(self, key: str) -> str:
        if not self._key_to_alt:
            self.markets()
        return self._key_to_alt.get(key, key)

    def tickers(self, market_ids: list[str]) -> list[Ticker]:
        result = self._get("/Ticker", {"pair": ",".join(market_ids)})
        now = datetime.now(timezone.utc)
        tickers = []
        for key, row in result.items():
            last = float(row["c"][0])
            volume_24h = float(row["v"][1])
            tickers.append(Ticker(market=self._alt(key), price=last,
                                  acc_trade_value_24h=last * volume_24h, ts=now))
        return tickers

    def hourly_candles(self, market_id: str, to: datetime) -> list[Candle]:
        """The most recent 720 hourly candles, whatever `to` is."""
        result = self._get("/OHLC", {"pair": market_id, "interval": 60})
        rows = next(v for k, v in result.items() if k != "last")
        return [Candle(
            market=market_id,
            start_at=datetime.fromtimestamp(int(r[0]), tz=timezone.utc),
            open=float(r[1]),
            high=float(r[2]),
            low=float(r[3]),
            close=float(r[4]),
            volume=float(r[6]),
        ) for r in rows]
