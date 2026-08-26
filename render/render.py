# -*- coding: utf-8 -*-
"""Compose the 4:5 "BEST LOOK" infographic from crops.json + a colorist JSON.

Photo slots (portrait, hair_3views, brows, eyes_5, contouring, before,
after_small) are placeholders here — Ф3 pastes nano-banana assets into the same
rects. Everything else (title, palette, swatches, text, footer) is drawn from
the analysis data with exact hex colours.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CROPS = os.path.join(ROOT, "template", "out", "crops.json")

# palette
BG        = "#FFFFFF"
INK       = "#1A1A1A"
BODY      = "#555555"
MUTE      = "#8A8A8A"
LINE      = "#E2E2E2"
PLACEHLD  = "#EAEEF2"
PLACETXT  = "#9AA6B2"

FONTS = {
    "reg":  r"C:\Windows\Fonts\arial.ttf",
    "bold": r"C:\Windows\Fonts\arialbd.ttf",
}
_cache = {}
def font(size, bold=False):
    key = (size, bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS["bold" if bold else "reg"], size)
    return _cache[key]


# ---- text helpers ------------------------------------------------------------
def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, fill, max_w, leading=1.3):
    lh = int(fnt.size * leading)
    for i, ln in enumerate(wrap(draw, text, fnt, max_w)):
        draw.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(wrap(draw, text, fnt, max_w)) * lh

def header(draw, x, y, text, size=26):
    draw.text((x, y), text.upper(), font=font(size, True), fill=INK)
    return y + int(size * 1.5)


# ---- swatch helpers ----------------------------------------------------------
def swatch_row(draw, x, y, w, h, colors, gap=6, radius=6):
    n = len(colors)
    cw = (w - gap * (n - 1)) / n
    for i, c in enumerate(colors):
        cx = x + i * (cw + gap)
        draw.rounded_rectangle([cx, y, cx + cw, y + h], radius=radius, fill=c)
    return cw

def circle(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color, outline="#00000018")


# ---- photo asset placement ---------------------------------------------------
def paste_contain(img, path, rect, pad=0):
    """Fit an image inside rect (keep aspect, no cropping), centered on white."""
    x, y, w, h = [int(v) for v in rect]
    w -= pad * 2; h -= pad * 2; x += pad; y += pad
    src = Image.open(path).convert("RGB")
    src.thumbnail((w, h), Image.LANCZOS)
    ox = x + (w - src.width) // 2
    oy = y + (h - src.height) // 2
    img.paste(src, (ox, oy))


def paste_cover(img, path, rect):
    """Fill rect completely (keep aspect, crop overflow), centered."""
    x, y, w, h = [int(v) for v in rect]
    src = Image.open(path).convert("RGB")
    scale = max(w / src.width, h / src.height)
    src = src.resize((max(1, int(src.width * scale)), max(1, int(src.height * scale))), Image.LANCZOS)
    cx = (src.width - w) // 2
    cy = (src.height - h) // 2
    img.paste(src.crop((cx, cy, cx + w, cy + h)), (x, y))


def caption_bar(draw, rect_, text, h=30):
    x, y, w, hh = [int(v) for v in rect_]
    draw.rectangle([x, y + hh - h, x + w, y + hh], fill=INK)
    f = font(16, True)
    tw = draw.textlength(text, font=f)
    draw.text((x + (w - tw) / 2, y + hh - h + 6), text, font=f, fill="#FFFFFF")


# ---- placeholder for photo slots --------------------------------------------
def placeholder(draw, rect, label, cells=None, cell_labels=None):
    x, y, w, h = rect
    draw.rectangle([x, y, x + w, y + h], fill=PLACEHLD, outline=LINE, width=2)
    if cells:
        for i, (cx, cy, cw, ch) in enumerate(cells):
            draw.rectangle([cx, cy, cx + cw, cy + ch], outline="#D3DAE0", width=2)
            if cell_labels and i < len(cell_labels):
                f = font(20, True)
                tw = draw.textlength(cell_labels[i], font=f)
                draw.text((cx + (cw - tw) / 2, cy + ch - 34), cell_labels[i],
                          font=f, fill=PLACETXT)
    f = font(24, True)
    tw = draw.textlength(label, font=f)
    draw.text((x + (w - tw) / 2, y + 14), label, font=f, fill=PLACETXT)


# ---- main --------------------------------------------------------------------
def render(analysis: dict, out_path: str, assets: dict | None = None, scale_out=None):
    assets = assets or {}
    crops = json.load(open(CROPS, encoding="utf-8"))
    S = crops["scale"]
    DW, DH = crops["design"]
    slots = crops["slots"]

    def rect(key):
        return [v / S for v in slots[key]["rect"]]

    def cells(key):
        return [[v / S for v in c] for c in slots[key].get("cells", [])]

    img = Image.new("RGB", (DW, DH), BG)
    d = ImageDraw.Draw(img)
    a = analysis

    # ---- title ----
    x, y, w, h = rect("title")
    t = "BEST LOOK"
    d.text((x + (w - d.textlength(t, font=font(64, True))) / 2, y + 14), t,
           font=font(64, True), fill=INK)
    sub = a["colortype"].upper()
    d.text((x + (w - d.textlength(sub, font=font(26, True))) / 2, y + 84), sub,
           font=font(26, True), fill=MUTE)

    # ---- section headers over photo-only blocks ----
    def slot_header(slot, text):
        x, y, w, h = rect(slot)
        d.text((x, y - 40), text.upper(), font=font(24, True), fill=INK)

    slot_header("hair_3views", "Recommended cut & color")
    slot_header("eyes_5", "Eyes — 5 looks")
    slot_header("contouring", "Contour")

    # ---- photo slots: real asset if present, else placeholder ----
    def photo(slot, label, fit="cover", cell_list=None, cell_labels=None, caption=None):
        r = rect(slot)
        if slot in assets and assets[slot] and os.path.exists(assets[slot]):
            (paste_cover if fit == "cover" else paste_contain)(img, assets[slot], r)
            if caption:
                caption_bar(d, r, caption)
            d.rectangle([r[0], r[1], r[0] + r[2], r[1] + r[3]], outline=LINE, width=2)
        else:
            placeholder(d, r, label, cell_list, cell_labels)

    photo("portrait", "AFTER — hero portrait", caption="AFTER")
    photo("before", "BEFORE (your photo)", caption="BEFORE")
    photo("after_small", "AFTER (crop)", caption="AFTER")
    photo("hair_3views", "CUT & COLOR", fit="cover",
          cell_list=cells("hair_3views"), cell_labels=["FRONT", "SIDE", "BACK"])
    photo("brows", "BROWS")
    photo("contouring", "CONTOUR")

    # eyes: 5 separate cells, each with a name caption strip
    eye_cells = cells("eyes_5")
    eye_imgs = assets.get("eyes_cells") or []
    if eye_imgs and all(os.path.exists(p) for p in eye_imgs):
        for i, (cx, cy, cw, ch) in enumerate(eye_cells):
            if i >= len(eye_imgs):
                break
            paste_cover(img, eye_imgs[i], (cx, cy, cw, ch))
            bar = 30
            d.rectangle([cx, cy + ch - bar, cx + cw, cy + ch], fill=INK)
            name = a["eyes"][i]["name"]
            f = font(16, True)
            tw = d.textlength(name, font=f)
            d.text((cx + (cw - tw) / 2, cy + ch - bar + 6), name, font=f, fill="#FFFFFF")
            d.rectangle([cx, cy, cx + cw, cy + ch], outline=LINE, width=2)
    else:
        placeholder(d, rect("eyes_5"), "EYES", eye_cells, [e["name"] for e in a["eyes"]])

    # ---- colortype + palette ----
    x, y, w, h = rect("colortype_palette")
    yy = header(d, x, y, "COLOR TYPE")
    d.text((x, yy), a["colortype"], font=font(38, True), fill=INK)
    yy += 52
    yy = text_block(d, x, yy, a["colortype_note"], font(21), BODY, w) + 12
    d.text((x, yy), "RECOMMENDED PALETTE", font=font(20, True), fill=INK)
    yy += 34
    pal = a["palette"]
    swatch_row(d, x, yy, w, 74, pal[:4], gap=10)
    swatch_row(d, x, yy + 84, w, 74, pal[4:], gap=10)

    # ---- hair color comparison ----
    x, y, w, h = rect("hair_swatches")
    half = (w - 60) / 2
    d.text((x, y), "BEFORE", font=font(18, True), fill=MUTE)
    d.text((x + half + 60, y), "AFTER", font=font(18, True), fill=MUTE)
    swatch_row(d, x, y + 24, half, h - 30, a["hair_color"]["before"], gap=4)
    swatch_row(d, x + half + 60, y + 24, half, h - 30, a["hair_color"]["after"], gap=4)
    # arrow
    ax = x + half + 18
    ay = y + 24 + (h - 30) / 2
    d.polygon([(ax, ay - 12), (ax + 26, ay), (ax, ay + 12)], fill=INK)

    # ---- brows tips ----
    x, y, w, h = rect("brows_tips")
    yy = header(d, x, y, "BROWS")
    d.text((x, yy), a["brows"]["shape"], font=font(22, True), fill=INK)
    yy += 40
    for tip in a["brows"]["tips"]:
        d.ellipse([x + 2, yy + 8, x + 10, yy + 16], fill=INK)
        yy = text_block(d, x + 22, yy, tip, font(20), BODY, w - 22) + 6

    # ---- contour swatches ----
    x, y, w, h = rect("contour_swatches")
    yy = header(d, x, y, "PRODUCTS", size=24)
    cs = a["contour_swatches"]
    items = [("Sculpt", cs["sculptor"]), ("Shadow", cs["shadow"]),
             ("Highlight", cs["highlighter"]), ("Blush", cs["blush"])]
    cw = (w - 30) / 4
    for i, (name, col) in enumerate(items):
        cx = x + i * (cw + 10)
        d.rounded_rectangle([cx, yy, cx + cw, yy + 64], radius=8, fill=col)
        f = font(17)
        tw = d.textlength(name, font=f)
        d.text((cx + (cw - tw) / 2, yy + 72), name, font=f, fill=BODY)

    # ---- lips ----
    x, y, w, h = rect("lips_6")
    yy = header(d, x, y, "LIPS — 6 SHADES")
    lips = a["lips"]
    cw = w / len(lips)
    for i, lip in enumerate(lips):
        cx = x + i * cw + cw / 2
        circle(d, cx, yy + 34, 30, lip["hex"])
        f = font(16)
        for j, ln in enumerate(wrap(d, lip["name"], f, cw - 8)):
            tw = d.textlength(ln, font=f)
            d.text((cx - tw / 2, yy + 74 + j * 18), ln, font=f, fill=BODY)

    # ---- footer (verdict header + 4 columns) ----
    x, y, w, h = rect("footer")
    d.line([(x, y), (x + w, y)], fill=INK, width=3)
    ttl = "THE VERDICT"
    d.text((x + (w - d.textlength(ttl, font=font(28, True))) / 2, y + 18), ttl,
           font=font(28, True), fill=INK)
    cy0 = y + 74
    cols = [("FACE & CUT", a["footer"]["face"]),
            ("HAIR COLOR", a["footer"]["hair"]),
            ("MAKEUP & BROWS", a["footer"]["makeup"]),
            ("STYLE", a["footer"]["style"])]
    cw = w / 4
    pad = 24
    for i, (hdr, body) in enumerate(cols):
        cx = x + i * cw + (0 if i == 0 else pad)
        if i:
            d.line([(x + i * cw, cy0), (x + i * cw, y + h - 8)], fill=LINE, width=1)
        d.text((cx, cy0), hdr, font=font(20, True), fill=INK)
        text_block(d, cx, cy0 + 34, body, font(19), BODY, cw - pad - 8)

    if scale_out and scale_out != DW:
        img = img.resize((scale_out, int(DH * scale_out / DW)), Image.LANCZOS)
    img.save(out_path)
    return out_path


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "tests", "_work", "analysis.json")
    data = json.load(open(src, encoding="utf-8"))
    out = os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    p = render(data, os.path.join(out, "preview.png"))
    print("saved ->", p)
