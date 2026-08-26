# -*- coding: utf-8 -*-
"""Discover the working kie.ai chat endpoint + model id.

Tries a few base URLs and model ids with a tiny vision request and reports which
combo returns a valid choices[].message.content. Run once, then paste the winner
into .env (KIE_BASE_URL / KIE_CHAT_MODEL).
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
KEY = os.environ["KIE_API_KEY"]
IMG = "https://i.ibb.co/35gXsLWR/f1e8a9ca5a89.jpg"

BASES = [
    "https://api.kie.ai/v1",
    "https://api.kie.ai",
]
MODELS = [
    "claude-sonnet-5", "claude-sonnet-4-5", "anthropic/claude-sonnet-5",
    "gpt-5.2", "gpt-5-2", "openai/gpt-5.2",
    "gemini-2.5-flash", "google/gemini-2.5-flash",
]


def try_combo(base, model):
    body = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "In one word, what is in this image?"},
                {"type": "image_url", "image_url": {"url": IMG}},
            ],
        }],
        "max_tokens": 50,
    }
    r = requests.post(f"{base}/chat/completions",
                      headers={"Authorization": f"Bearer {KEY}"},
                      json=body, timeout=60)
    ok = False
    txt = ""
    try:
        j = r.json()
        txt = j["choices"][0]["message"]["content"]
        ok = True
    except Exception:
        txt = r.text[:200]
    return r.status_code, ok, txt


if __name__ == "__main__":
    for base in BASES:
        for model in MODELS:
            try:
                code, ok, txt = try_combo(base, model)
            except Exception as e:
                code, ok, txt = "ERR", False, str(e)[:120]
            mark = "OK " if ok else "-- "
            print(f"{mark}[{code}] {base}  {model:28s} -> {str(txt)[:80]}")
            if ok:
                print(f"\n>>> WINNER: KIE_BASE_URL={base}  KIE_CHAT_MODEL={model}")
                raise SystemExit(0)
    print("\nNo combo worked — check the model catalog at kie.ai/market/chat")
