# -*- coding: utf-8 -*-
"""Thread-safe progress shared between the worker thread (pipeline) and the
event-loop animator that edits the Telegram status message."""
import threading
import time

# key -> checklist label (order = display order). "eyes" is special (X/5).
STEPS = [
    ("analysis", "Colour type decoded"),
    ("portrait", "Hero portrait"),
    ("hair_3views", "Hair & colour"),
    ("brows", "Brows"),
    ("eyes", "Eye makeup"),
    ("contouring", "Contour map"),
    ("render", "Final assembly"),
]
TOTAL_UNITS = 11  # analysis(1) + 4 single assets + 5 eyes + render(1)


class Progress:
    def __init__(self, eyes_total=5):
        self._lock = threading.Lock()
        self.state = {k: "pending" for k, _ in STEPS}
        self.eyes_done = 0
        self.eyes_total = eyes_total
        self.finished = False
        self.start = time.time()

    def set(self, key, status):
        with self._lock:
            self.state[key] = status

    def eye_done(self):
        with self._lock:
            self.eyes_done += 1
            self.state["eyes"] = "done" if self.eyes_done >= self.eyes_total else "active"

    def snapshot(self):
        with self._lock:
            return dict(self.state), self.eyes_done, self.eyes_total, self.finished

    def fraction(self):
        st, ed, et, _ = self.snapshot()
        done = 1 if st["analysis"] == "done" else 0
        for k in ("portrait", "hair_3views", "brows", "contouring"):
            done += 1 if st[k] == "done" else 0
        done += ed
        done += 1 if st["render"] == "done" else 0
        return done / TOTAL_UNITS
