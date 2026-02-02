# Gold Standard Prompts for Generative Creative Engine
# Verified on 2026-01-31

# 1. T-Shirt Design Generation
# Context: Used by Creative Director / ImageGenService
DESIGN_PROMPT_TEMPLATE = (
    "T-shirt design graphic, {keyword} theme, {style} style, "
    "featuring {elements}, color palette: {palette}, {mood} atmosphere, "
    "Studio flash with holographic reflections, vector art, high definition, "
    "detailed texture, isolated on white background, no mockup, flat 2d --v 6.0"
)

# 2. Virtual Try-On (VTON) Simulation
# Context: Used by NanoBananaService
VTON_PROMPT_TEMPLATE = (
    "A photorealistic medium shot of a stylish young man walking on a street in Tokyo. "
    "He is wearing a white t-shirt that features the EXACT {keyword} pattern shown in the reference image. "
    "The pattern is printed clearly on the chest of the shirt. "
    "Natural lighting, 8k resolution, cinematic composition."
)

# 3. Video Synthesis (Sora 2)
# Context: Used by SoraService
# Updated to reflect User's Motion Transfer Request (Ref: Pexels 5899702)
# STRICT: 15 seconds, preserve Design Asset, VTON fidelity.
VIDEO_PROMPT_TEMPLATE = (
    "Sora 2 Motion Transfer: Use the specific motion from reference video (Runway Walk). "
    "Apply this motion to the VTON input image (Man wearing {keyword} shirt). "
    "Ensure the Design Asset is fully visible on the chest throughout the walk. "
    "Maintain photorealistic texture and high-fashion lighting. Duration: 15s."
)
