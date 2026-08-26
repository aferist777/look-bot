# -*- coding: utf-8 -*-
"""Quick 5x2 contact sheet of the 10 catalog thumbnails for review."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from colorist.catalog import CATALOG

THUMBS = os.path.join(ROOT, "catalog", "thumbs")
CW, CH, COLS = 320, 400, 5
LABEL = 34
rows = (len(CATALOG) + COLS - 1) // COLS
sheet = Image.new("RGB", (CW * COLS, (CH + LABEL) * rows), "white")
d = ImageDraw.Draw(sheet)
try:
    f = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)
except OSError:
    f = ImageFont.load_default()

for i, look in enumerate(CATALOG):
    r, c = divmod(i, COLS)
    x, y = c * CW, r * (CH + LABEL)
    p = os.path.join(THUMBS, f"{look['id']}.png")
    if os.path.exists(p):
        im = Image.open(p).convert("RGB")
        im.thumbnail((CW, CH), Image.LANCZOS)
        sheet.paste(im, (x + (CW - im.width) // 2, y))
    d.text((x + 8, y + CH + 6), f"{look['name']}", font=f, fill="black")

out = os.path.join(THUMBS, "_montage.png")
sheet.save(out)
print("montage ->", out)
