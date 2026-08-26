# -*- coding: utf-8 -*-
"""One-call pipeline: local photo (+intent) -> final 4:5 infographic path."""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from colorist.imgbb import upload_image
from colorist.agent import analyze
from colorist.style_agent import analyze_style
from colorist.assets import build_assets
from colorist.stats import record
from render.render import render


def run_pipeline(photo_path: str, intent: str | None, work_dir: str,
                 resolution: str = "2K", progress=None, look: dict | None = None) -> tuple[str, dict]:
    """Full generation. Returns (final_png_path, analysis_dict).

    look: optional catalog look dict -> fitting-room (style) mode instead of the
    honest colour analysis. progress: optional Progress for live status.
    """
    t0 = time.time()
    os.makedirs(work_dir, exist_ok=True)

    if progress:
        progress.set("analysis", "active")
    ref_url = upload_image(photo_path)
    if look:
        analysis = analyze_style(ref_url, look).model_dump()
    else:
        analysis = analyze(ref_url, user_intent=intent or None).model_dump()
    if progress:
        progress.set("analysis", "done")

    assets = build_assets(analysis, ref_url, work_dir, resolution=resolution, progress=progress)
    assets["before"] = photo_path
    assets["after_small"] = assets["portrait"]

    if progress:
        progress.set("render", "active")
    out = os.path.join(work_dir, "final.png")
    render(analysis, out, assets=assets)
    if progress:
        progress.set("render", "done")
        progress.finished = True

    record(time.time() - t0)
    return out, analysis
