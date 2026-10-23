"""Paper-trade executor. Appends to trades/paper_trades.json. Never real."""
import json
import os
from datetime import datetime, timezone


class PaperTrader:
    def __init__(self, log_path):
        self.log_path = log_path

    def execute(self, setup, ai1_confidence, ai2_confidence, ai2_source):
        trade = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mode": "paper",
            "symbol": setup.get("symbol", "BTC/USD"),
            "direction": setup["direction"],
            "entry": setup["entry"],
            "stop_loss": setup["stop_loss"],
            "take_profit": setup["take_profit"],
            "rr": setup["rr"],
            "ai1_confidence": ai1_confidence,
            "ai2_confidence": ai2_confidence,
            "ai2_source": ai2_source,
            "result": "open",
        }
        trades = []
        if os.path.exists(self.log_path):
            with open(self.log_path) as f:
                trades = json.load(f)
        trade["id"] = len(trades) + 1
        trades.append(trade)
        with open(self.log_path, "w") as f:
            json.dump(trades, f, indent=2)
        return trade
