# -*- coding: utf-8 -*-
"""Fitting-room agent: restyle THIS person into a catalog look -> ColoristAnalysis.

Unlike the honest colorist (agent.py), this does NOT report the person's natural
season — it renders the TARGET style's own recipe (its colortype label, hair,
brows, eyes, contour, lips, palette) applied to the user's face."""
import json

from pydantic import ValidationError

from .agent import _extract_json
from .client import KieChat
from .schema import ColoristAnalysis, schema_hint

STYLE_SYSTEM = """\
You are a senior celebrity stylist, colourist and makeup artist. You are given a \
portrait of a person and a TARGET STYLE brief. Restyle THIS person into that \
style and produce a complete "BEST LOOK" breakdown that fully embodies the \
target style — NOT the person's natural season.

Keep the person's face and identity recognisable, and read their CURRENT hair \
colour from the photo for the before-comparison, but every recommendation \
(haircut, hair colour, brows, the 5 eye looks, contour, lips, palette and the \
colortype label) must express the TARGET STYLE.

OUTPUT RULES:
- Respond in ENGLISH only. Return a SINGLE JSON object and NOTHING else (no \
markdown, no code fences, no commentary).
- Match the provided JSON schema EXACTLY: same keys, exact list lengths, within \
every maxLength. Every colour is a #RRGGBB hex.
- colortype = the 12-season label named in the brief (closest match).
- hair_color.before = 6 swatches of the person's CURRENT observed hair; \
hair_color.after = 6 swatches of the STYLE's hair colour.
- eyes = EXACTLY 5 makeup looks in the STYLE, soft→bold. Each gen_prompt must \
describe a CLEARLY VISIBLE, well-defined makeup look (name shadow colours, liner, \
lashes) so it is obvious on camera — saturated, not barely-there.
- gen_prompts.portrait = a prompt to generate THIS person restyled in the target \
style (its hair colour/cut and signature makeup), photoreal, clean light. \
gen_prompts.hair_3views = front/side/back of the style's haircut on this person.
- lips, contour_swatches, palette, footer all follow the target style.
- Do NOT restate the schema. Output only the data.
"""


def analyze_style(image_url: str, look: dict, client: KieChat | None = None,
                  retries: int = 2) -> ColoristAnalysis:
    client = client or KieChat()
    base_text = (
        f"TARGET STYLE — {look['name']}:\n{look['brief']}\n\n"
        "Restyle the person in this portrait into the TARGET STYLE and return a "
        "single JSON object conforming EXACTLY to this schema (keys, list lengths, "
        "maxLength, hex):\n\n" + schema_hint()
    )
    user_text = base_text
    last_err = None
    for _ in range(retries + 1):
        raw = client.vision_json(STYLE_SYSTEM, user_text, image_url, json_mode=False)
        try:
            return ColoristAnalysis.model_validate(_extract_json(raw))
        except (ValidationError, json.JSONDecodeError) as e:
            last_err = e
            user_text = (base_text + "\n\nYour previous answer was INVALID. Fix "
                         "these problems and return corrected JSON only:\n" + str(e)[:1500])
    raise RuntimeError(f"style agent failed validation after {retries + 1} tries: {last_err}")
