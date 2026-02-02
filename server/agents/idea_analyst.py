import random
from typing import Dict, Any, List

class IdeaAnalyst:
    """
    Simulates an AI agent that extracts design concepts from trends.
    Uses 'Design Personas' to vary the output style.
    """
    
    PERSONAS = [
        {
            "name": "The Minimalist",
            "style": "Clean, Sans-serif, High Contrast",
            "focus": "Typography and Negative Space",
            "mood": "Sophisticated"
        },
        {
            "name": "The Retro Futurist",
            "style": "Synthwave, Neon, Glitch Art",
            "focus": "80s Anime aesthetics and grid lines",
            "mood": "Nostalgic"
        },
        {
            "name": "The Grunge Artist",
            "style": "Distressed, Texture-heavy, Collage",
            "focus": "Raw emotion and chaotic layout",
            "mood": "Rebellious"
        },
        {
            "name": "The Nature Lover",
            "style": "Organic, Botanical, Soft Lines",
            "focus": "Plant life and natural color palettes",
            "mood": "Calm"
        }
    ]

    def analyze(self, trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes a single trend item using a random Design Persona.
        Returns a rich structural analysis (V4).
        """
        persona = random.choice(self.PERSONAS)
        trend_title = trend_data.get("title", "Unknown Trend")
        
        # Simulate Deep Analysis
        return {
            "meta": {
                "persona": persona['name'],
                "trend_source": trend_title,
                "mood": persona['mood']
            },
            "rationale": {
                "headline": f"Reimagining {trend_title} through a {persona['name']} lens.",
                "content": f"The '{trend_title}' trend typically focuses on mass appeal, but by applying {persona['name']} principles, we strip away the noise. We focus on {persona['focus']} to create a piece that feels both timely and timeless. This approach disrupts the standard market offering by adding a layer of {persona['mood']} sophistication."
            },
            "dimensions": {
                "commercial_viability": "High potential for urban demographics aged 18-30. Strong crossover appeal with tech-focused lifestyle brands.",
                "target_audience": "Creative professionals, skaters, and digital nomads who value aesthetic precision over loud branding.",
                "color_psychology": f"The palette ({self._generate_palette(persona['name'])}) uses contrasting temperatures to evoke a sense of balanced energy typical of the {persona['mood']} mood."
            },
            "composition": {
                "layout": "Asymmetrical, maximizing negative space to draw the eye.",
                "foreground": f"Abstract {persona['focus']} interpretation.",
                "typography": "Swiss-style sans-serif, kerning loosened for modern feel."
            },
            "prompt": f"T-shirt design, {trend_title}, {persona['style']}, {persona['focus']}, {persona['mood']} atmosphere, vector art, high definition, detailed texture, isolated on white background",
            "attributes": { # Keep legacy flat attributes for backward compat if needed
                "Theme": f"{trend_title} x {persona['name']}",
                "Style": persona['style'],
                "Palette": self._generate_palette(persona['name'])
            }
        }

    def _generate_palette(self, persona_name: str) -> str:
        if "Retro" in persona_name:
            return "Hot Pink #FF00FF, Cyan #00FFFF, Deep Purple #330099"
        elif "Minimalist" in persona_name:
            return "Black #000000, White #FFFFFF, Slate #64748B"
        elif "Nature" in persona_name:
            return "Sage Green #84A98C, Earth Brown #6B4423, Cream #F4F1DE"
        else:
            return "Charcoal #333333, Crimson #DC143C, Distressed Grey #A9A9A9"

    def batch_analyze(self, trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.analyze(t) for t in trends]

if __name__ == "__main__":
    analyst = IdeaAnalyst()
    mock_trend = {"title": "Cyberpunk Aesthetics"}
    print(json.dumps(analyst.analyze(mock_trend), indent=2))
