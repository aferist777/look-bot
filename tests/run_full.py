# -*- coding: utf-8 -*-
"""Ф3 end-to-end: photo (+intent) -> colorist JSON -> 5 nano assets -> final 4:5."""
import json
import os
import sys

from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

from colorist.imgbb import upload_image
from colorist.agent import analyze
from colorist.assets import build_assets
from render.render import render

WORK = os.path.join(os.path.dirname(__file__), "_work")
os.makedirs(WORK, exist_ok=True)


def main():
    photo = os.path.join(os.path.dirname(__file__), "reference_girl.jpg")
    intent = os.environ.get("INTENT", "I want to look more feminine")

    ref_url = os.environ.get("REF_URL") or upload_image(photo)
    print(f"Ref URL: {ref_url}\nIntent : {intent}")

    ana_path = os.path.join(WORK, "analysis_full.json")
    if os.environ.get("REUSE_ANALYSIS") and os.path.exists(ana_path):
        analysis = json.load(open(ana_path, encoding="utf-8"))
        print("Analysis: reused")
    else:
        print("Colorist analysing ...")
        analysis = analyze(ref_url, user_intent=intent).model_dump()
        json.dump(analysis, open(ana_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Season: {analysis['colortype']}")

    print("Generating nano-banana assets ...")
    assets = build_assets(analysis, ref_url, WORK, resolution=os.environ.get("RES", "2K"))
    assets["before"] = photo
    assets["after_small"] = assets["portrait"]

    out = os.path.join(WORK, "final.png")
    render(analysis, out, assets=assets)
    print(f"\nDONE -> {out}")


if __name__ == "__main__":
    main()
