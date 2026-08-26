# -*- coding: utf-8 -*-
"""nano-banana-2 image generation via kie.ai (createTask + poll recordInfo)."""
import json
import os
import time
import requests

CREATE = "https://api.kie.ai/api/v1/jobs/createTask"
INFO = "https://api.kie.ai/api/v1/jobs/recordInfo"


def generate(prompt: str, image_input=None, aspect_ratio="1:1",
             resolution="2K", output_format="png",
             api_key=None, poll=4, timeout=360) -> str:
    """Create a nano-banana-2 task, poll to completion, return the result URL."""
    key = api_key or os.environ["KIE_API_KEY"]
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {
        "model": "nano-banana-2",
        "input": {
            "prompt": prompt,
            "image_input": image_input or [],
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "output_format": output_format,
        },
    }
    r = requests.post(CREATE, headers=headers, json=body, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"createTask {r.status_code}: {r.text[:400]}")
    task_id = r.json()["data"]["taskId"]

    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(poll)
        g = requests.get(INFO, headers=headers, params={"taskId": task_id}, timeout=60).json()
        data = g.get("data") or {}
        state = data.get("state")
        if state == "success":
            urls = json.loads(data["resultJson"]).get("resultUrls", [])
            if not urls:
                raise RuntimeError(f"success but no resultUrls: {data}")
            return urls[0]
        if state == "fail":
            raise RuntimeError(f"nano-banana failed: {data.get('failMsg')} ({data.get('failCode')})")
    raise TimeoutError(f"task {task_id} not finished in {timeout}s")
