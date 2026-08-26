# -*- coding: utf-8 -*-
"""Render the animated checklist status message (Variant 2, light-flirt tone)."""
from .progress import STEPS

ICON = {"done": "✅", "active": "🔄", "pending": "⬜"}

HYPE = [
    "Serving looks, loading… 💅",
    "Almost that girl… ✨",
    "Main-character energy loading… 😘",
    "Trust the process, gorgeous ✨",
    "Worth the wait, promise 😘",
    "Beauty takes a sec 💋",
    "Cooking up something pretty… 🔥",
]


def _fmt(sec: float) -> str:
    sec = max(0, int(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def render_status(progress, eta_est: float, tick: int) -> str:
    st, ed, et, _ = progress.snapshot()
    remaining = max(1, round(eta_est * (1 - progress.fraction())))

    lines = ["💫 Building your BEST LOOK…", "", HYPE[tick % len(HYPE)], ""]
    for key, label in STEPS:
        if key == "eyes":
            state = "done" if ed >= et else ("active" if ed > 0 or st["eyes"] == "active" else "pending")
            lines.append(f"{ICON[state]} {label} — {ed}/{et}")
        else:
            lines.append(f"{ICON[st[key]]} {label}")
    lines += ["", f"⏳ ~{_fmt(remaining)} left"]
    return "\n".join(lines)
