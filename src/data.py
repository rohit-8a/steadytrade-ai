"""Market data: OHLC candles from the Bitstamp public API (no key needed)."""
import requests


def fetch_ohlc(symbol="BTC/USD", timeframe="3600", limit=48):
    """Return the last `limit` OHLC candles for `symbol`, oldest first."""
    # Bitstamp's OHLC endpoint expects `step` in seconds; accept human labels too.
    steps = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400, "1d": 86400}
    step = steps.get(str(timeframe).lower(), timeframe)
    pair = symbol.replace("/", "").lower()
    url = f"https://www.bitstamp.net/api/v2/ohlc/{pair}/"
    resp = requests.get(url, params={"step": step, "limit": limit}, timeout=15)
    resp.raise_for_status()
    rows = resp.json()["data"]["ohlc"]
    return [
        {
            "timestamp": int(c["timestamp"]),
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"]),
            "volume": float(c["volume"]),
        }
        for c in rows
    ]
