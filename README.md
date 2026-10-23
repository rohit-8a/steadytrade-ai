# SteadyTrade AI 🦥

**Hacktoberfest 2026 — Week 3 "Slow and Steady" Open-Source AI Challenge submission**

A two-AI confirmation trading bot. No impulsive trades: every signal must pass
**two independent AI gates** before a (paper) trade is placed. Slow and steady
wins.

## How it works

```
Market data (OHLC, Bitstamp public API)
      │
      ▼
┌──────────────┐
│    AI #1     │  Chart analysis → confidence score (0–100%)
│  Gatekeeper  │  If confident: suggests 3 risk-reward setups
└──────┬───────┘
       │  confidence ≥ 60% ?
       ├── No  → ⛔ STOP. Trade declined, pipeline ends here.
       ▼ Yes
┌──────────────┐
│    AI #2     │  Compares the 3 setups against YOUR past trades
│  Decision    │  (Laya open-weight decision model, runs locally)
└──────┬───────┘  → picks the single best risk-reward setup
       │  final confidence ≥ 60% ?
       ├── No  → ⛔ STOP. No trade.
       ▼ Yes → ✅ PAPER trade executed and logged
```

## The two AI gates

1. **AI #1 — Chart Analyst** (`src/ai_chart.py`): reads recent OHLC candles,
   outputs a confidence score and, when confident, 3 candidate setups
   (entry / stop-loss / take-profit at RR 1:1.5, 1:2, 1:3).
   Below 60% → the trade is **declined and everything stops right there**.
2. **AI #2 — Decision Maker** (`src/ai_decision.py`): takes the 3 setups plus
   the log of past trades, asks the **Laya** open-weight model to compare
   them, and selects the best risk-reward setup. Needs ≥ 60% final
   confidence, otherwise no trade.

## Open-source AI at the core

- **Laya** (Convai open-weight System-1 decision model, runs locally on CPU)
  powers AI #2 — real model, zero API cost.
- AI #1 ships with a transparent indicator-based baseline (`BASELINE` in
  `src/ai_chart.py`) behind a clean `analyze()` interface, ready to swap for
  an open-weight chart/vision model.

## Safety

- **Paper trading only.** `mode: "paper"` in `config.yaml`. No real orders,
  no real money. This is an educational project.

## Run

```bash
pip install -r requirements.txt
python -m src.main
```

## Project layout

```
steadytrade-ai/
├── config.yaml            # thresholds, symbol, mode (paper only)
├── requirements.txt
├── src/
│   ├── data.py            # OHLC fetch (Bitstamp public API, no key)
│   ├── ai_chart.py        # AI #1: chart analysis → confidence + 3 RR setups
│   ├── ai_decision.py     # AI #2: Laya compares setups vs past trades
│   ├── trader.py          # paper-trade executor + gate logic
│   └── main.py            # pipeline orchestration
├── trades/
│   ├── past_trades.json   # your trade history (AI #2 learns from this)
│   └── paper_trades.json  # trades this bot places (created on run)
└── DEV_POST_TEMPLATE.md   # submission post draft for dev.to
```
