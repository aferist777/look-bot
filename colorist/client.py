# -*- coding: utf-8 -*-
"""Thin client for kie.ai's chat (LLM) API — OpenAI-compatible style.

kie.ai exposes leading chat models (Claude / GPT / Gemini) behind one key. The
exact base URL / model id is confirmed via probe.py and stored in .env
(KIE_BASE_URL, KIE_CHAT_MODEL). This wrapper keeps the rest of the code stable.
"""
import os
import requests

DEFAULT_BASE = "https://api.kie.ai/v1"


class KieChat:
    def __init__(self, api_key=None, base_url=None, model=None, timeout=120):
        self.api_key = api_key or os.environ["KIE_API_KEY"]
        self.base_url = (base_url or os.environ.get("KIE_BASE_URL") or DEFAULT_BASE).rstrip("/")
        self.model = model or os.environ.get("KIE_CHAT_MODEL")
        self.timeout = timeout

    def vision_json(self, system: str, user_text: str, image_url: str,
                    json_mode: bool = True, max_tokens: int = 6000) -> str:
        """Send a system + (text, image) user turn, return the assistant text."""
        content = [
            {"type": "text", "text": user_text},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": content},
            ],
            "temperature": 0.4,
            "max_tokens": max_tokens,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}

        resp = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}",
                     "Content-Type": "application/json"},
            json=body, timeout=self.timeout,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"kie chat {resp.status_code}: {resp.text[:500]}")
        data = resp.json()
        if "choices" not in data:
            raise RuntimeError(f"kie chat unexpected response: {str(data)[:500]}")
        return data["choices"][0]["message"]["content"]
