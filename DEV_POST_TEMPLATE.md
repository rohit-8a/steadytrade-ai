# DEV submission post — template (write it in YOUR words; judging weights writing quality)

> Publish on dev.to as your Week 3 challenge entry. Link your GitHub repo.
> Suggested title: "I Built a Trading Bot That Refuses to Trade 🦥"

---

## The problem (2-3 lines)
Most trading bots are trigger-happy. I wanted the opposite: a bot that is
**slow and steady** — one that says "no trade" far more often than "trade".

## The idea (short)
Two independent AI gates must BOTH agree before a single (paper) trade happens:

1. **AI #1 — Chart Analyst.** Reads recent OHLC candles, scores confidence
   0–100%. Below 60% → trade declined, pipeline stops right there.
   At 60%+ → it suggests 3 risk-reward setups (RR 1:1.5, 1:2, 1:3).
2. **AI #2 — Decision Maker (Laya, open-weight, runs locally).** Compares the
   3 setups against my own past-trade log, picks the single best
   risk-reward setup. Needs 60%+ final confidence or no trade.

Kill switch: if AI #1 declines, everything stops. No second chances.

## Open-source AI at the core
- **Laya** (Convai open-weight System-1 decision model) — AI #2, local CPU.
- AI #1 chart analysis behind a swappable `analyze()` interface (baseline
  indicator heuristic included, ready for an open-weight chart model).

## How I built it (keep honest & specific)
- Data: Bitstamp public OHLC API (no key).
- Stack: Python, PyYAML, requests. Paper trades logged to JSON.
- Hard rule: `mode: "paper"` — the project **cannot** place real orders.

## Demo / results
[Paste: a real run log — AI #1 confidence, the 3 setups, AI #2's pick,
final decision. Screenshots of terminal output help.]

## What I learned
[2-4 honest lines: what surprised you, what broke, what you'd improve.]

## Repo
[GitHub link]

## What's next
[1-2 lines: e.g. swap AI #1 baseline for an open-weight vision model,
backtest on 1 year of data.]
