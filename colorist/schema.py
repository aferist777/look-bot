# -*- coding: utf-8 -*-
"""Strict schema for the colorist analysis.

Every text field is length-capped so it fits its slot in the 4:5 layout; every
colour is a validated #RRGGBB hex; list lengths are exact. Validation failures
are fed back to the model for a retry (see agent.py).
"""
from typing import Annotated, List, Literal
from pydantic import BaseModel, StringConstraints, Field

# 12-season colour analysis system
SUBSEASON = Literal[
    "Light Spring", "Warm Spring", "Bright Spring",
    "Light Summer", "Cool Summer", "Soft Summer",
    "Soft Autumn", "Warm Autumn", "Deep Autumn",
    "Bright Winter", "Cool Winter", "Deep Winter",
]

Hex = Annotated[str, StringConstraints(pattern=r"^#[0-9A-Fa-f]{6}$")]


def txt(n: int):
    return Annotated[str, StringConstraints(min_length=1, max_length=n, strip_whitespace=True)]


class Haircut(BaseModel):
    name: txt(28)
    desc: txt(160)


class HairColor(BaseModel):
    before: List[Hex] = Field(min_length=6, max_length=6)
    after: List[Hex] = Field(min_length=6, max_length=6)


class Brows(BaseModel):
    shape: txt(30)
    tips: List[txt(70)] = Field(min_length=4, max_length=4)


class EyeLook(BaseModel):
    name: txt(20)
    gen_prompt: txt(400)   # instruction for nano-banana (this makeup, lashes included)


class Contouring(BaseModel):
    zones: txt(120)
    gen_prompt: txt(400)


class ContourSwatches(BaseModel):
    sculptor: Hex
    shadow: Hex
    highlighter: Hex
    blush: Hex


class LipShade(BaseModel):
    name: txt(22)
    hex: Hex


class Footer(BaseModel):
    face: txt(180)
    hair: txt(180)
    makeup: txt(180)
    style: txt(180)


class GenPrompts(BaseModel):
    portrait: txt(600)
    hair_3views: txt(600)


class ColoristAnalysis(BaseModel):
    colortype: SUBSEASON
    colortype_note: txt(160)          # short justification (undertone/contrast/value)
    face_shape: txt(20)
    haircut: Haircut
    hair_color: HairColor
    brows: Brows
    eyes: List[EyeLook] = Field(min_length=5, max_length=5)
    contouring: Contouring
    contour_swatches: ContourSwatches
    lips: List[LipShade] = Field(min_length=6, max_length=6)
    palette: List[Hex] = Field(min_length=8, max_length=8)
    footer: Footer
    gen_prompts: GenPrompts


# JSON schema string handed to the model so it knows the exact contract.
def schema_hint() -> str:
    import json
    return json.dumps(ColoristAnalysis.model_json_schema(), ensure_ascii=False, indent=2)
