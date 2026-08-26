# -*- coding: utf-8 -*-
"""Fitting-room catalog: 10 collective looks. Each look carries its OWN full
style recipe (hair, brows, eyes, contour, lips, palette, season label) that the
style agent turns into a complete BEST LOOK breakdown on the user's face.

Briefs grounded in style research (clean girl, e-girl, K-beauty from web;
others from standard editorial/makeup practice)."""

CATALOG = [
    {
        "id": "clean_girl",
        "name": "Clean girl",
        "emoji": "🤍",
        "tagline": "Effortless, glossy, expensive-looking",
        "brief": (
            "CLEAN GIRL aesthetic. Neutral undertone, luminous dewy 'glass' skin, "
            "no-makeup makeup. Hair: healthy glossy brunette/bronde, sleek slicked-"
            "back low bun with a centre part, or a smooth glassy blowout. Brows: "
            "laminated, brushed-up, fluffy, natural taupe-brown. Eyes: minimal — "
            "soft neutral wash, brown mascara, feathery lashes, thin tightline; even "
            "the bolder looks stay soft (soft bronze, subtle brown liner, wet sheen). "
            "Lips: glossy 'your-lips-but-better' nudes and rosy nudes with soft liner. "
            "Contour: soft cream bronzer, cream blush high on the cheeks, dewy "
            "highlight. Palette: neutral beige, soft white, camel, taupe, soft rose. "
            "Season label: Soft Summer (neutral)."),
        "thumb_prompt": (
            "Beauty portrait of a young woman, clean-girl aesthetic: dewy glass skin, "
            "glossy nude lips, fluffy laminated brows, slicked-back glossy low bun, "
            "minimal neutral makeup, soft daylight, plain beige background"),
    },
    {
        "id": "old_money",
        "name": "Old-money brunette",
        "emoji": "🥂",
        "tagline": "Quiet luxury, soft glam, understated",
        "brief": (
            "OLD-MONEY quiet-luxury look. Neutral-warm, polished satin skin, soft "
            "glam. Hair: rich glossy brunette with subtle dimension, soft bouncy "
            "blowout, face-framing layers, expensive shine. Brows: neatly groomed, "
            "softly defined, natural. Eyes: refined neutrals — matte taupe and soft "
            "brown shadow, subtle definition, wispy natural lashes, thin tightline; "
            "sophisticated, never flashy. Lips: rosy-brown MLBB, soft satin nudes. "
            "Contour: softly sculpted cheekbones, muted rosy-brown blush, subtle "
            "highlight. Palette: camel, cream, navy, chocolate, burgundy, soft gold. "
            "Season label: Soft Autumn."),
        "thumb_prompt": (
            "Elegant woman, old-money quiet-luxury beauty, soft glam neutral makeup, "
            "glossy brunette blowout, groomed brows, rosy-brown lip, refined, cream "
            "background"),
    },
    {
        "id": "copper_ginger",
        "name": "Copper goddess",
        "emoji": "🔥",
        "tagline": "Warm copper, bronze glow, freckles",
        "brief": (
            "COPPER / GINGER GODDESS. Warm undertone celebrated. Hair: vibrant "
            "copper-ginger red, glossy, soft waves. Brows: soft auburn-brown, natural. "
            "Eyes: warm — bronze, copper and terracotta shadows, warm soft-smoky "
            "blend, bronze/brown liner, defined lashes, sunlit. Lips: brick, "
            "terracotta, warm coral, cinnamon. Contour: warm bronzer, peachy-"
            "terracotta blush, gold highlight, soft faux freckles. Palette: rust, "
            "olive, mustard, cream, forest green, terracotta. Season label: Warm "
            "Autumn."),
        "thumb_prompt": (
            "Woman with vibrant copper ginger wavy hair, warm bronze eye makeup, "
            "freckles, terracotta lip, sunlit glow, plain background"),
    },
    {
        "id": "blonde_bombshell",
        "name": "Blonde bombshell",
        "emoji": "💛",
        "tagline": "Hollywood glam, bold lip, cat-eye",
        "brief": (
            "BLONDE BOMBSHELL Hollywood glam. Hair: luminous buttery/champagne "
            "blonde, voluminous glamorous waves, deep side part. Brows: defined, "
            "groomed, softly arched. Eyes: classic glam — neutral-to-smoky lid, "
            "precise black winged cat-eye, full dramatic lashes, inner-corner "
            "highlight. Lips: bold classic red and polished pink-nudes. Contour: "
            "sculpted cheekbones, warm blush, strong highlight. Palette: red, black, "
            "gold, ivory, champagne, cobalt. Season label: Bright Winter."),
        "thumb_prompt": (
            "Glamorous blonde woman, Hollywood glam, voluminous blonde waves, black "
            "winged cat-eye, bold red lip, sculpted cheekbones, studio glam light"),
    },
    {
        "id": "soft_romantic",
        "name": "Soft romantic",
        "emoji": "🌸",
        "tagline": "Rosy, feathered, feminine",
        "brief": (
            "SOFT ROMANTIC feminine look. Cool-neutral, soft. Hair: soft light-brown "
            "brunette, romantic loose curls, curtain bangs, face-framing. Brows: "
            "soft, feathered, natural. Eyes: rosy-mauve and soft pink shadows, soft "
            "rounded doll definition, soft brown liner, fluttery lashes — romantic, "
            "never sharp. Lips: rose, mauve pink, soft berry, glossy. Contour: soft "
            "pink blush on the apples, gentle sculpt, dewy. Palette: blush pink, "
            "lavender, rose, soft blue, pearl, mauve. Season label: Cool Summer."),
        "thumb_prompt": (
            "Romantic feminine beauty, soft brunette curls with curtain bangs, rosy "
            "pink eye makeup, mauve glossy lip, soft blush, dreamy soft light"),
    },
    {
        "id": "egirl",
        "name": "E-girl",
        "emoji": "🖤",
        "tagline": "Graphic liner, heavy blush, bold",
        "brief": (
            "E-GIRL grunge-anime fusion. Cool-toned. Hair: dark base with a bright "
            "split-dye or bleached money-piece (pink/blue/platinum), often straight "
            "with front curtain framing. Brows: straight, defined. Eyes: sharp thin "
            "graphic winged liner, pastel or smoky shadow, faux freckles, doll-like; "
            "bolder looks use floating graphic liner. Signature HEAVY 'drunk' blush "
            "across the nose and under the eyes, wet highlight. Lips: blurred "
            "popsicle peach or glossy. Contour: heavy pink blush over nose and cheeks, "
            "sharp highlight. Palette: black, hot pink, electric blue, lilac, silver, "
            "white. Season label: Bright Winter."),
        "thumb_prompt": (
            "E-girl makeup, sharp thin winged eyeliner, heavy pink blush across nose "
            "and cheeks, faux freckles, split-dye hair with pink money-piece, "
            "cool-toned, plain background"),
    },
    {
        "id": "sultry_smoky",
        "name": "Sultry smoky",
        "emoji": "🌙",
        "tagline": "Deep smoky eye, vamp, sculpted",
        "brief": (
            "SULTRY SMOKY high-drama look. Hair: dark brunette to black, glossy, "
            "sleek and voluminous. Brows: defined, groomed. Eyes: deep diffused "
            "smoky eye (charcoal, espresso, plum), fully blended, dramatic lashes, "
            "optional subtle shimmer at centre — a sultry bedroom eye. Lips: vamp "
            "berry and deep rose, plus a nude-brown to balance. Contour: strongly "
            "sculpted cheek and jaw, bronzed, defined. Palette: black, deep plum, "
            "charcoal, wine, gunmetal, nude. Season label: Deep Winter."),
        "thumb_prompt": (
            "Sultry smoky eye makeup, deep charcoal blended smokey eyes, sculpted "
            "contour, glossy dark hair, vamp nude lip, moody low light"),
    },
    {
        "id": "beachy_bronde",
        "name": "Sun-kissed beachy",
        "emoji": "☀️",
        "tagline": "Bronde waves, coral, glowy",
        "brief": (
            "SUN-KISSED BEACHY look. Warm-neutral, glowy. Hair: bronde (blonde-brown "
            "balayage), tousled beach waves, sun-lightened ends. Brows: soft, "
            "natural, sun-kissed. Eyes: warm golden-bronze soft wash, peachy tones, "
            "soft smudged liner, natural fluttery lashes, glowy. Lips: coral, peach, "
            "warm nude gloss. Contour: warm bronzer, peachy-coral blush, dewy gold "
            "highlight, soft faux freckles. Palette: coral, turquoise, sand, gold, "
            "white, denim blue. Season label: Warm Spring."),
        "thumb_prompt": (
            "Sun-kissed beachy beauty, bronde tousled beach waves, glowy bronze "
            "makeup, coral lip, freckles, golden-hour light"),
    },
    {
        "id": "editorial_bold",
        "name": "Editorial bold",
        "emoji": "🎨",
        "tagline": "Colour-pop eye, sculpted, high-fashion",
        "brief": (
            "EDITORIAL BOLD high-fashion look. Hair: sleek modern high-shine, "
            "structured (dark or statement). Brows: sculpted, gelled, editorial. "
            "Eyes: bold colour-pop graphic eyeshadow in jewel tones (cobalt, emerald, "
            "fuchsia) or high-gloss lids — artistic and statement. Lips: a clean nude "
            "to balance a bold eye, or a matching bold shade. Contour: strong "
            "editorial sculpt, glassy skin, high highlight. Palette: cobalt, emerald, "
            "fuchsia, black, silver, ivory. Season label: Bright Spring."),
        "thumb_prompt": (
            "High-fashion editorial beauty, bold cobalt graphic eyeshadow, sculpted "
            "glassy skin, sleek hair, statement makeup, studio editorial light"),
    },
    {
        "id": "kbeauty_gradient",
        "name": "K-beauty glow",
        "emoji": "🍑",
        "tagline": "Glass skin, gradient lip, straight brows",
        "brief": (
            "K-BEAUTY youthful glow. Dewy luminous glass skin. Hair: glossy soft "
            "brown or black, airy, straight or soft waves. Brows: straight, softly "
            "filled, low arch, neutral. Eyes: soft rosy/peach or coral wash, aegyo-sal "
            "under-eye puff highlight, subtle definition, natural lashes — youthful. "
            "Lips: gradient blurred lip (rose/coral/pink) with a diffused centre. "
            "Contour: diffused blush placed near the centre of the face, minimal "
            "contour, dewy. Palette: peach, coral, rose, soft pink, ivory, mint. "
            "Season label: Light Spring."),
        "thumb_prompt": (
            "Korean K-beauty makeup, dewy glass skin, gradient coral lip, straight "
            "soft brows, aegyo-sal under-eye highlight, glossy soft brown hair, "
            "youthful, soft light"),
    },
]

BY_ID = {look["id"]: look for look in CATALOG}
