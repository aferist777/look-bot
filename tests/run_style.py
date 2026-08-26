# -*- coding: utf-8 -*-
"""Test the fitting-room (style) pipeline end-to-end on the reference photo.
Usage: python tests/run_style.py <look_id>   (default: egirl)"""
import os
import sys

from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

from colorist.catalog import BY_ID
from colorist.pipeline import run_pipeline


def main():
    look_id = sys.argv[1] if len(sys.argv) > 1 else "egirl"
    look = BY_ID[look_id]
    photo = os.path.join(os.path.dirname(__file__), "reference_girl.jpg")
    work = os.path.join(os.path.dirname(__file__), "_style", look_id)

    print(f"Style: {look['name']}")
    out, analysis = run_pipeline(photo, None, work, resolution="2K", look=look)
    print(f"colortype label: {analysis['colortype']}")
    print(f"hair after: {analysis['hair_color']['after']}")
    print(f"eyes: " + ", ".join(e['name'] for e in analysis['eyes']))
    print(f"DONE -> {out}")


if __name__ == "__main__":
    main()
