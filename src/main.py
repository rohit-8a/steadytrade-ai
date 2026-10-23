"""SteadyTrade AI pipeline: data -> AI #1 gate -> AI #2 gate -> paper trade."""
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data import fetch_ohlc
from src.ai_chart import ChartAnalyst
from src.ai_decision import DecisionMaker
from src.trader import PaperTrader

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    with open(os.path.join(BASE, "config.yaml")) as f:
        cfg = yaml.safe_load(f)
    assert cfg["mode"] == "paper", "Live trading is disabled in this project."

    print("Fetching market data...")
    candles = fetch_ohlc(cfg["symbol"], timeframe=cfg["timeframe"], limit=cfg["candles"])
    print(f"  {len(candles)} candles, last close {candles[-1]['close']}")

    # ---- AI #1: chart analysis (gatekeeper) ----
    ai1 = ChartAnalyst(cfg)
    confidence, setups = ai1.analyze(candles)
    print(f"AI #1 confidence: {confidence}%")
    if confidence < cfg["ai1_min_confidence"]:
        print("⛔ AI #1 declined the trade. Stopping here — no trade.")
        return
    print(f"AI #1 confirmed. Suggested {len(setups)} RR setups.")

    # ---- AI #2: compare setups vs past trades (Laya) ----
    with open(os.path.join(BASE, "trades", "past_trades.json")) as f:
        past_trades = json.load(f)
    ai2 = DecisionMaker(cfg)
    best, final_conf, source = ai2.decide(setups, past_trades)
    print(f"AI #2 ({source}) picked {best['id']} "
          f"(RR 1:{best['rr']}) with {final_conf}% confidence.")
    if final_conf < cfg["ai2_min_confidence"]:
        print("⛔ AI #2 confidence below gate. No trade.")
        return

    # ---- Paper trade ----
    best["symbol"] = cfg["symbol"]
    trader = PaperTrader(os.path.join(BASE, "trades", "paper_trades.json"))
    trade = trader.execute(best, confidence, final_conf, source)
    print(f"✅ PAPER trade #{trade['id']} logged: {best['direction']} "
          f"@ {best['entry']} (RR 1:{best['rr']}).")


if __name__ == "__main__":
    main()
