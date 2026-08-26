# -*- coding: utf-8 -*-
"""Generate the 5 nano-banana photo assets for the layout, with a local cache."""
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor

import requests

from .nano import generate

STYLE = ("Photoreal, natural skin texture, soft even studio light, plain light "
         "background, sharp focus, no text, no watermark, no labels.")


def _brows_prompt(a):
    b = a["brows"]
    return (f"Extreme close-up of ONE eyebrow and eye area of this person, brow "
            f"shape '{b['shape']}', groomed and softly defined. {STYLE}")


EYE_BASE_PROMPT = (
    "Extreme close-up of the person's LEFT eye and LEFT eyebrow only, filling the "
    "frame, completely BARE with absolutely NO makeup. Reproduce the EXACT eye "
    "shape, eyelid crease, lash line, iris colour and eyebrow shape from the "
    "reference photo — do not alter them. Straight-on angle, neutral even "
    "lighting, plain light background. " + STYLE)


def _eye_prompt(e):
    return (f"Using the referenced LEFT eye as the exact base, keep the eye shape, "
            f"eyelid, crease, iris colour and eyebrow IDENTICAL — do not change the "
            f"eye itself. Apply a CLEARLY VISIBLE, well-defined {e['name']} eye "
            f"makeup that reads obviously on camera: {e['gen_prompt']} Make the "
            f"eyeshadow, liner and lashes distinct and saturated (not subtle). Same "
            f"tight close-up framing on the same left eye, plain background. {STYLE}")


def specs(a):
    """Single-image assets (one nano call each)."""
    return {
        "portrait":    dict(prompt=a["gen_prompts"]["portrait"] + " " + STYLE, aspect_ratio="1:1"),
        "hair_3views": dict(prompt=a["gen_prompts"]["hair_3views"] +
                            " Front, side and back views of the hairstyle in one "
                            "horizontal image, evenly spaced. " + STYLE,
                            aspect_ratio="16:9"),
        "brows":       dict(prompt=_brows_prompt(a), aspect_ratio="3:2"),
        "contouring":  dict(prompt=a["contouring"]["gen_prompt"] +
                            " Face-mapping contour scheme drawn on the face, "
                            "plain neutral background. " + STYLE,
                            aspect_ratio="1:1"),
    }


def _download(url, path):
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)
    return path


def build_assets(analysis: dict, ref_url: str, work_dir: str,
                 resolution="2K", use_cache=True, progress=None, max_workers=9) -> dict:
    """Generate every photo asset IN PARALLEL; return {slot: local_png_path}.

    progress (colorist.progress.Progress) is updated per asset so the bot can
    animate a live checklist.
    """
    os.makedirs(work_dir, exist_ok=True)
    cache_file = os.path.join(work_dir, "assets.json")
    cache = {}
    if use_cache and os.path.exists(cache_file):
        cache = json.load(open(cache_file, encoding="utf-8"))
    cache_lock = threading.Lock()
    urls = {}  # key -> nano result URL (used to chain the eye base into the 5 looks)

    def _get(key, prompt, aspect, ref_urls):
        local = os.path.join(work_dir, f"{key}.png")
        if use_cache and key in cache and os.path.exists(local):
            print(f"  [cache] {key}")
            urls[key] = cache[key]
            return local
        print(f"  [gen]   {key} ({aspect}) ...")
        url = generate(prompt, image_input=ref_urls, aspect_ratio=aspect, resolution=resolution)
        _download(url, local)
        with cache_lock:
            cache[key] = url
            urls[key] = url
            json.dump(cache, open(cache_file, "w", encoding="utf-8"), indent=2)
        return local

    def gen_single(slot, spec):
        if progress:
            progress.set(slot, "active")
        path = _get(slot, spec["prompt"], spec["aspect_ratio"], [ref_url])
        if progress:
            progress.set(slot, "done")
        return slot, path

    def gen_eye_base():
        # one clean, makeup-free eye that fixes the shape for all 5 looks
        if progress:
            progress.set("eyes", "active")
        _get("eye_base", EYE_BASE_PROMPT, "1:1", [ref_url])
        return urls["eye_base"]

    def gen_eye(i, e, base_url):
        path = _get(f"eye_{i}", _eye_prompt(e), "1:1", [base_url])
        if progress:
            progress.eye_done()
        return i, path

    out = {}
    eyes = [None] * len(analysis["eyes"])
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        single_futs = [ex.submit(gen_single, s, sp) for s, sp in specs(analysis).items()]
        base_fut = ex.submit(gen_eye_base)
        base_url = base_fut.result()  # eyes depend on the base; singles keep running
        eye_futs = [ex.submit(gen_eye, i, e, base_url) for i, e in enumerate(analysis["eyes"])]
        for f in single_futs:
            slot, path = f.result()
            out[slot] = path
        for f in eye_futs:
            i, path = f.result()
            eyes[i] = path
    out["eyes_cells"] = eyes
    return out
