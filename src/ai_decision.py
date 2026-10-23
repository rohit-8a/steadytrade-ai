"""AI #2 — Decision Maker (Laya open-weight decision model).

Compares the 3 setups AI #1 suggested against the log of past trades and
picks the single best risk-reward setup. Falls back to plain expectancy
math when Laya is unavailable (marked in the output).
"""
import json
import subprocess


class DecisionMaker:
    def __init__(self, config):
        self.cfg = config

    def _past_stats(self, past_trades):
        wins = [t for t in past_trades if t.get("result") == "win"]
        total = len(past_trades)
        win_rate = (len(wins) / total * 100) if total else 50.0
        avg_rr = (sum(t.get("setup_rr", 0) for t in past_trades) / total) if total else 2.0
        return {"trades": total, "win_rate": round(win_rate, 1), "avg_rr": round(avg_rr, 2)}

    def _laya_decide(self, state_text):
        schema = {
            "best_setup": {"enum": ["setup_1", "setup_2", "setup_3"]},
            "take_trade": {"type": "boolean"},
        }
        cmd = [self.cfg["laya_python"], self.cfg["laya_consult"],
               state_text, json.dumps(schema)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        proc.check_returncode()
        return json.loads(proc.stdout)

    def _fallback(self, setups, stats):
        # Expectancy = win_rate * rr - (1 - win_rate); pick the best.
        wr = stats["win_rate"] / 100.0
        scored = [(s, wr * s["rr"] - (1 - wr)) for s in setups]
        best = max(scored, key=lambda x: x[1])[0]
        conf = round(max(0.0, min(0.99, wr * best["rr"] / 3.0)) * 100, 1)
        return best, conf, "fallback"

    def decide(self, setups, past_trades):
        """Return (best_setup, confidence 0-100, source)."""
        stats = self._past_stats(past_trades)
        lines = [
            f"You are choosing ONE trade setup. Past performance: "
            f"{stats['trades']} trades, {stats['win_rate']}% win rate, "
            f"average RR {stats['avg_rr']}.",
            "Candidate setups:",
        ]
        for s in setups:
            lines.append(
                f"- {s['id']}: {s['direction']} entry {s['entry']}, "
                f"SL {s['stop_loss']}, TP {s['take_profit']}, RR 1:{s['rr']}"
            )
        lines.append("Pick the setup with the best risk-reward given the past "
                     "performance. Only say take_trade=true if you are confident.")
        try:
            res = self._laya_decide("\n".join(lines))
            best = next(s for s in setups if s["id"] == res["values"]["best_setup"])
            # consult.py returns per-field confidences (0-1); scale best_setup's.
            conf = round(float(res["confidence"]["best_setup"]) * 100, 1)
            if not res["values"]["take_trade"]:
                conf = min(conf, 59.9)  # model says no -> stays below the gate
            return best, conf, "laya"
        except Exception:
            return self._fallback(setups, stats)
