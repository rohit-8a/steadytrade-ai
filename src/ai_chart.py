"""AI #1 — Chart Analyst (gatekeeper).

Interface: analyze(candles) -> (confidence 0-100, setups[])

The BASELINE below is a transparent indicator heuristic. Swap it for an
open-weight chart/vision model by replacing analyze() — the rest of the
pipeline does not change.
"""


class ChartAnalyst:
    def __init__(self, config):
        self.cfg = config

    # ---- BASELINE: replace with an open-weight model for the real build ----
    def _sma(self, values, n):
        return sum(values[-n:]) / n

    def _atr(self, candles, n=14):
        trs = []
        for i in range(1, len(candles)):
            h, l, pc = candles[i]["high"], candles[i]["low"], candles[i - 1]["close"]
            trs.append(max(h - l, abs(h - pc), abs(l - pc)))
        return sum(trs[-n:]) / n

    def analyze(self, candles):
        closes = [c["close"] for c in candles]
        price = closes[-1]
        sma20 = self._sma(closes, 20)
        roc = (price - closes[-12]) / closes[-12] * 100      # 12-candle momentum %
        atr = self._atr(candles)
        atr_pct = atr / price * 100

        # Confidence heuristic (documented, deterministic):
        # trend alignment 40% + momentum 35% + volatility penalty 25%
        trend_score = max(0.0, min(1.0, (price - sma20) / (atr * 2) + 0.5))
        mom_score = max(0.0, min(1.0, roc / 4.0 + 0.5))
        vol_score = max(0.0, min(1.0, 1.0 - atr_pct / 6.0))
        confidence = round((trend_score * 40 + mom_score * 35 + vol_score * 25), 1)

        setups = []
        if confidence >= self.cfg["ai1_min_confidence"]:
            for i, rr in enumerate([1.5, 2.0, 3.0], start=1):
                risk = atr * 1.5
                setups.append({
                    "id": f"setup_{i}",
                    "direction": "long" if price >= sma20 else "short",
                    "entry": round(price, 2),
                    "stop_loss": round(price - risk, 2),
                    "take_profit": round(price + risk * rr, 2),
                    "rr": rr,
                })
        return confidence, setups
