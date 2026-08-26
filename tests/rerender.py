# -*- coding: utf-8 -*-
"""Re-render final.png from cached analysis + assets (no nano calls) — for layout iteration."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from render.render import render

WORK = os.path.join(os.path.dirname(__file__), "_work")


def main():
    analysis = json.load(open(os.path.join(WORK, "analysis_full.json"), encoding="utf-8"))

    def p(name):
        return os.path.join(WORK, name)

    assets = {
        "portrait": p("portrait.png"),
        "hair_3views": p("hair_3views.png"),
        "brows": p("brows.png"),
        "contouring": p("contouring.png"),
        "before": os.path.join(os.path.dirname(__file__), "reference_girl.jpg"),
        "eyes_cells": [p(f"eye_{i}.png") for i in range(5)],
    }
    assets["after_small"] = assets["portrait"]

    out = p("final.png")
    render(analysis, out, assets=assets)
    print("re-rendered ->", out)


if __name__ == "__main__":
    main()
