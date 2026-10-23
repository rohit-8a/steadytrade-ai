# I Built a Trading Bot That Refuses to Trade 🦥

Every trading bot I've seen is trigger-happy. Green candle? BUY. Red candle? SELL. Most of them trade like they're in a hurry to lose money.

Week 3's theme is **"Slow and Steady"** — so I built the opposite: a bot that says "no trade" far more often than "trade." Meet **SteadyTrade AI**.

## The idea

Two independent AI gates. **BOTH** must agree, or nothing happens:

🚦 **AI #1 — The Gatekeeper.** Reads recent BTC candles and scores its confidence from 0–100%. Below 60%? Trade declined. Full stop — the pipeline ends right there. No second opinions, no maybes. At 60% or above, it suggests 3 risk-reward setups (RR 1:1.5, 1:2, 1:3).

🧠 **AI #2 — The Decision Maker.** Takes those 3 setups plus my own past-trade log and asks **Laya** — an open-weight decision model running locally on my machine — to pick the single best risk-reward setup. Final confidence needs 60%+, or still no trade.

Most days, this bot does nothing. That's the point. 🦥

## Open-source AI at the core

- **Laya** (Convai's open-weight System-1 decision model) powers AI #2. Real model, local CPU, zero API cost.
- AI #1 sits behind a clean `analyze()` interface — it ships with a transparent indicator-based baseline, ready to swap for an open-weight chart/vision model.

No black boxes calling paid APIs. Everything runs on my own machine.

## How it's built

- **Data:** Bitstamp public OHLC API (no key needed), 48 recent 1-hour candles.
- **Stack:** Python, `requests`, PyYAML. Every decision is logged to JSON, so the bot's history feeds back into AI #2's next decision.
- **Hard rule:** `mode: "paper"` in the config. This project **cannot** place real orders — it's educational by design.

The pipeline in one look:

```
Market data → AI #1 (≥60%?) → 3 RR setups → AI #2 + past trades (≥60%?)
→ PAPER trade logged ... or silence. Usually silence.
```

## First run

Real terminal output from a live test run (`python -m src.main`), 21 Oct 2026:

```
Fetching market data...
  48 candles, last close 83435.07
AI #1 confidence: 85.4%
AI #1 confirmed. Suggested 3 RR setups.
AI #2 (laya) picked setup_1 (RR 1:1.5) with 12.0% confidence.
⛔ AI #2 confidence below gate. No trade.
```

AI #1 was confident (85.4%) and suggested 3 setups — but Laya only gave the
best setup 12.0% confidence, so the gate fired and the bot did nothing.
That's the whole point of the design: two gates, and most days the answer
is silence. (In an earlier pre-fix run, the fallback path logged PAPER trade
#1 at 62.5% — visible in `trades/paper_trades.json` with `"mode": "paper"`.)

## What I learned

I learned that building a bot is easy, but teaching it when NOT to trade is the real work — my two gates said no more often than yes, and that felt right.

The biggest surprise came in my first real run: AI #1 was 85% confident, but Laya gave only 12%, so no trade happened. Two AIs can look at the same data and completely disagree.

I also learned to keep learning safe — paper mode means I can test every idea without risking a single rupee.

## What's next

- Swap AI #1's baseline for a real open-weight chart model.
- Backtest the two-gate logic on a year of BTC data.
- Track how often the gatekeeper says no — and whether the trades it *allows* actually perform better.

## Repo

🔗 https://github.com/rohit-8a/steadytrade-ai

---

*Built for the Hacktoberfest 2026 Week 3 "Slow and Steady" Open-Source AI Challenge. Slow and steady wins. 🦥*
