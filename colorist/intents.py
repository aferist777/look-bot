# -*- coding: utf-8 -*-
"""Optional user-goal handling + example prompts shown in the bot upload message."""

# Shown to the user when the bot asks for a photo, so they know they CAN add a
# free-text goal and how to phrase it. English (bot UI is English).
EXAMPLE_INTENTS = [
    "I want to look more feminine",
    "I want to look younger",
    "I want a bolder, more striking look",
    "I want a soft, natural everyday look",
    "I want to look more elegant / expensive",
    "I want to look more confident",
]

UPLOAD_MESSAGE = (
    "Send me a clear, front-facing selfie in natural light (no filters, hair "
    "off the face).\n\n"
    "Optional: add a caption with what you want, for example:\n"
    + "\n".join(f"• {x}" for x in EXAMPLE_INTENTS)
    + "\n\nI'll analyse your colouring and build your personal BEST LOOK."
)
