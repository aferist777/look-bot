# -*- coding: utf-8 -*-
"""Generate the 10 catalog thumbnails once (2K, 4:5), saved to catalog/thumbs/."""
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import requests
from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

from colorist.catalog import CATALOG
from colorist.nano import generate

THUMBS = os.path.join(ROOT, "catalog", "thumbs")
os.makedirs(THUMBS, exist_ok=True)

STYLE = ("Photoreal beauty portrait, single young woman, head and shoulders, "
         "sharp focus, flattering light. No text, no watermark.")


def one(look):
    path = os.path.join(THUMBS, f"{look['id']}.png")
    if os.path.exists(path):
        print(f"  [skip] {look['id']}")
        return look["id"], path
    print(f"  [gen]  {look['id']} ...")
    url = generate(look["thumb_prompt"] + " " + STYLE, image_input=[],
                   aspect_ratio="4:5", resolution="2K")
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    open(path, "wb").write(r.content)
    return look["id"], path


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=10) as ex:
        list(ex.map(one, CATALOG))
    print("thumbs ->", THUMBS)
