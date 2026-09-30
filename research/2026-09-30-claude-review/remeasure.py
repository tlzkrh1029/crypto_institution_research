"""Re-measure the rank-bucket comparison and the Upbit volume share.

Reproduces the numbers in market-remeasure.md. Uses only free public APIs
(CoinGecko /coins/markets without a key, Upbit /v1/ticker). Running it later
produces a new snapshot, not the 2026-09-30 12:39 KST numbers.

Usage:
    python3 remeasure.py                         # fetch live data
    python3 remeasure.py --coingecko-json cg.json --no-upbit
    python3 remeasure.py --csv snapshot.csv
"""

import argparse
import csv
import json
import statistics
import sys
import time
import urllib.request

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/coins/markets"
    "?vs_currency=usd&per_page=150&page=1&price_change_percentage=24h,7d,30d"
)
UPBIT_MARKETS_URL = "https://api.upbit.com/v1/market/all"
UPBIT_TICKER_URL = "https://api.upbit.com/v1/ticker?markets="

# Tokens cited in the review. XRP is the same-narrative control; AVAX, ENA and
# ALGO were looked up after the fact, so they are illustrations, not a
# pre-registered control group.
WATCH = ["BTC", "ETH", "XRP", "LINK", "XLM", "HBAR", "QNT", "ONDO",
         "ALGO", "AVAX", "ENA", "SOL"]

# Stablecoins, gold-backed tokens and fund tokens excluded by symbol.
EXCLUDED_SYMBOLS = {
    "usdt", "usdc", "dai", "usde", "usds", "fdusd", "pyusd", "tusd", "usd1",
    "rlusd", "usdtb", "susde", "susds", "xaut", "paxg", "bsc-usd", "usdf",
    "usdg", "buidl", "usyc", "ousg", "syrupusdc", "gho", "frax", "usd0",
    "crvusd", "eurc", "lusd",
}
# Wrapped, staked, bridged and similar derivative tokens excluded by id.
EXCLUDED_ID_PARTS = [
    "wrapped", "staked", "bridged", "liquid-staked", "usd-coin", "tether",
    "gold", "restaked", "binance-peg", "coinbase-wrapped", "lido", "jito",
    "rocket-pool", "mantle-staked", "ether-fi", "kelp", "renzo", "solv",
    "lombard",
]

BUCKETS = [("1-10", 1, 10), ("11-50", 11, 50), ("51-100", 51, 100)]


def fetch_json(url, retries=3, wait_sec=8):
    last_error = None
    for _ in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
            return json.loads(body)
        except (ValueError, OSError) as exc:  # "Throttled" is not JSON
            last_error = exc
            time.sleep(wait_sec)
    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def is_excluded(coin):
    if coin["symbol"].lower() in EXCLUDED_SYMBOLS:
        return True
    coin_id = coin["id"].lower()
    return any(part in coin_id for part in EXCLUDED_ID_PARTS)


def median(values):
    values = [v for v in values if v is not None]
    return round(statistics.median(values), 2) if values else None


def bucket_table(coins):
    kept = [c for c in coins if not is_excluded(c)][:100]
    rows = []
    for name, lo, hi in BUCKETS:
        members = [c for c in kept
                   if c.get("market_cap_rank") and lo <= c["market_cap_rank"] <= hi]
        r24 = [c.get("price_change_percentage_24h_in_currency") for c in members]
        rows.append({
            "bucket": name,
            "n": len(members),
            "median_24h": median(r24),
            "median_7d": median([c.get("price_change_percentage_7d_in_currency") for c in members]),
            "median_30d": median([c.get("price_change_percentage_30d_in_currency") for c in members]),
            "up_24h": sum(1 for v in r24 if v is not None and v > 0),
        })
    return rows


def watch_table(coins):
    by_symbol = {}
    for c in coins:
        by_symbol.setdefault(c["symbol"].upper(), c)  # first hit = highest rank
    rows = []
    for sym in WATCH:
        c = by_symbol.get(sym)
        if c is None:
            rows.append({"symbol": sym, "rank": None})
            continue

        def pct(key):
            v = c.get(key)
            return None if v is None else round(v, 2)

        rows.append({
            "symbol": sym,
            "rank": c.get("market_cap_rank"),
            "chg_24h": pct("price_change_percentage_24h_in_currency"),
            "chg_7d": pct("price_change_percentage_7d_in_currency"),
            "chg_30d": pct("price_change_percentage_30d_in_currency"),
            "volume_usd": c.get("total_volume"),
            "market_cap_usd": c.get("market_cap"),
            "last_updated": c.get("last_updated"),
        })
    return rows


def upbit_shares(watch_rows):
    listed = {m["market"] for m in fetch_json(UPBIT_MARKETS_URL)
              if m["market"].startswith("KRW-")}
    symbols = [r["symbol"] for r in watch_rows if f"KRW-{r['symbol']}" in listed]
    markets = [f"KRW-{s}" for s in symbols] + ["KRW-USDT"]
    tickers = {t["market"].split("-")[1]: t
               for t in fetch_json(UPBIT_TICKER_URL + ",".join(markets))}
    usdt_krw = tickers["USDT"]["trade_price"]
    for r in watch_rows:
        t = tickers.get(r["symbol"])
        if t is None:
            r["upbit_listed"] = False
            continue
        r["upbit_listed"] = True
        upbit_usd = t["acc_trade_price_24h"] / usdt_krw
        r["upbit_volume_usd"] = round(upbit_usd)
        if r.get("volume_usd"):
            r["upbit_share_pct"] = round(upbit_usd / r["volume_usd"] * 100, 1)
    return usdt_krw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--coingecko-json", help="use a saved /coins/markets response")
    parser.add_argument("--no-upbit", action="store_true")
    parser.add_argument("--csv", help="write the watch table to this CSV path")
    args = parser.parse_args()

    if args.coingecko_json:
        with open(args.coingecko_json, encoding="utf-8") as f:
            coins = json.load(f)
    else:
        coins = fetch_json(COINGECKO_URL)

    print("bucket   n  median_24h  median_7d  median_30d  up_24h")
    for b in bucket_table(coins):
        print(f"{b['bucket']:7} {b['n']:3}  {b['median_24h']:>10}  {b['median_7d']:>9}"
              f"  {b['median_30d']:>10}  {b['up_24h']:>6}")

    watch = watch_table(coins)
    if not args.no_upbit:
        usdt_krw = upbit_shares(watch)
        print(f"\nUpbit USDT/KRW: {usdt_krw}")

    print("\nsymbol  rank   chg_24h   chg_7d  chg_30d  upbit_share_pct")
    for r in watch:
        if r.get("rank") is None:
            print(f"{r['symbol']:6}  not in fetched range")
            continue
        share = r.get("upbit_share_pct", "not listed" if r.get("upbit_listed") is False else "-")
        print(f"{r['symbol']:6} {r['rank']:5} {r['chg_24h']:>9} {r['chg_7d']:>8}"
              f" {r['chg_30d']:>8}  {share}")

    if args.csv:
        fields = ["symbol", "rank", "chg_24h", "chg_7d", "chg_30d", "volume_usd",
                  "market_cap_usd", "last_updated", "upbit_listed",
                  "upbit_volume_usd", "upbit_share_pct"]
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(watch)
    return 0


if __name__ == "__main__":
    sys.exit(main())
