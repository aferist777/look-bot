# -*- coding: utf-8 -*-
"""Upload a local image to imgbb and return a public URL.

kie.ai's image_input wants URLs, not bytes, so every user photo (and every
generated asset we want to feed back as a reference) goes through here first.
"""
import base64
import os
import requests

IMGBB_ENDPOINT = "https://api.imgbb.com/1/upload"


def upload_image(path: str, api_key: str | None = None, expiration: int | None = None) -> str:
    """Upload `path` to imgbb, return the direct image URL.

    expiration: optional seconds (60..15552000) after which imgbb deletes it.
    """
    api_key = api_key or os.environ["IMGBB_API_KEY"]
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    params = {"key": api_key}
    if expiration:
        params["expiration"] = expiration

    resp = requests.post(IMGBB_ENDPOINT, params=params, data={"image": b64}, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"imgbb upload failed: {data}")
    return data["data"]["url"]


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    print(upload_image(sys.argv[1]))
