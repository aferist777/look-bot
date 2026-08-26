# -*- coding: utf-8 -*-
"""Adaptive ETA: EMA of past full-run durations, persisted to stats.json."""
import json
import os
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS = os.path.join(ROOT, "stats.json")
DEFAULT_ETA = 90.0     # cold-start seconds
_lock = threading.Lock()


def load_estimate() -> float:
    try:
        return float(json.load(open(STATS, encoding="utf-8"))["eta"])
    except Exception:
        return DEFAULT_ETA


def record(actual_seconds: float, alpha: float = 0.3) -> float:
    with _lock:
        cur = load_estimate()
        new = alpha * actual_seconds + (1 - alpha) * cur
        try:
            json.dump({"eta": round(new, 1)}, open(STATS, "w", encoding="utf-8"))
        except Exception:
            pass
        return new
