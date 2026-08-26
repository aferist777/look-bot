# -*- coding: utf-8 -*-
"""Ф1 end-to-end test: local photo -> imgbb -> colorist -> validated JSON."""
import json
import os
import sys

from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

from colorist.imgbb import upload_image
from colorist.agent import analyze

WORK = os.path.join(os.path.dirname(__file__), "_work")
os.makedirs(WORK, exist_ok=True)


def main():
    photo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "reference_girl.jpg")

    # allow reusing an already-hosted url to skip re-upload
    url = os.environ.get("REF_URL")
    if not url:
        print(f"Uploading {photo} ...")
        url = upload_image(photo)
    print(f"Image URL: {url}")

    print("Analysing (colorist agent) ...")
    result = analyze(url)

    out = os.path.join(WORK, "analysis.json")
    with open(out, "w", encoding="utf-8") as f:
        f.write(result.model_dump_json(indent=2))

    d = result.model_dump()
    print("\n=== COLORIST RESULT ===")
    print(f"Season:   {d['colortype']}  ({d['colortype_note']})")
    print(f"Face:     {d['face_shape']}")
    print(f"Haircut:  {d['haircut']['name']} — {d['haircut']['desc']}")
    print(f"Hair now: {d['hair_color']['before']}")
    print(f"Hair rec: {d['hair_color']['after']}")
    print(f"Brows:    {d['brows']['shape']} | " + " / ".join(d['brows']['tips']))
    print(f"Eyes:     " + ", ".join(e['name'] for e in d['eyes']))
    print(f"Lips:     " + ", ".join(f"{l['name']}({l['hex']})" for l in d['lips']))
    print(f"Palette:  {d['palette']}")
    print(f"Footer:   {d['footer']}")
    print(f"\nSaved -> {out}")


if __name__ == "__main__":
    main()
