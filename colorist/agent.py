# -*- coding: utf-8 -*-
"""Colorist agent: portrait image URL -> validated ColoristAnalysis."""
import json
import re

from pydantic import ValidationError

from .client import KieChat
from .prompt import SYSTEM_PROMPT
from .schema import ColoristAnalysis, schema_hint

USER_TEXT = (
    "Analyse this portrait and return the BEST LOOK breakdown as a single JSON "
    "object that conforms EXACTLY to this JSON schema (keys, list lengths, "
    "maxLength, hex format):\n\n" + schema_hint()
)


def _extract_json(s: str) -> dict:
    s = s.strip()
    if s.startswith("```"):                       # strip accidental fences
        s = re.sub(r"^```[a-zA-Z]*\n?|\n?```$", "", s).strip()
    start, end = s.find("{"), s.rfind("}")
    if start != -1 and end != -1:
        s = s[start:end + 1]
    return json.loads(s)


def analyze(image_url: str, user_intent: str | None = None,
            client: KieChat | None = None, retries: int = 2) -> ColoristAnalysis:
    client = client or KieChat()
    base_text = USER_TEXT
    if user_intent:
        base_text += (
            f'\n\nThe user\'s stated goal: "{user_intent.strip()}". '
            "Steer the haircut, colour, makeup, lips and palette toward this "
            "goal while keeping the seasonal analysis honest."
        )
    user_text = base_text
    last_err = None

    for attempt in range(retries + 1):
        raw = client.vision_json(SYSTEM_PROMPT, user_text, image_url, json_mode=False)
        try:
            return ColoristAnalysis.model_validate(_extract_json(raw))
        except (ValidationError, json.JSONDecodeError) as e:
            last_err = e
            # feed the exact problem back for a corrected retry
            user_text = (
                base_text
                + "\n\nYour previous answer was INVALID. Fix these problems and "
                "return corrected JSON only:\n" + str(e)[:1500]
            )
    raise RuntimeError(f"colorist failed validation after {retries + 1} tries: {last_err}")
