import random
from typing import Dict, Any, List

class CreativeDirectorAgent:
    """
    The 'Brain' of the Generative Engine.
    Synthesizes T-Shirt Design Specifications purely from trend keywords.
    Simulates an LLM's vast knowledge base of visual styles.
    """
    
    # "Simulated LLM" Knowledge Base
    # In a real production env, this would be RAG + GPT-4.
    STYLE_KNOWLEDGE_BASE = {
        "y2k": {
            "style": "Y2K Aesthetic",
            "palette": ["#FF1493", "#00FFFF", "#C0C0C0", "#000000"], # Hot Pink, Cyan, Silver, Black
            "elements": "chrome text, fluid tribal shapes, butterfly motifs, pixel art glitches",
            "mood": "Playful, Nostalgic, Cyber-pop",
            "lighting": "Studio flash with holographic reflections"
        },
        "cyberpunk": {
            "style": "Cyberpunk Futurism",
            "palette": ["#FF0055", "#00F0FF", "#121212", "#FAFAFA"],
            "elements": "circuit board patterns, neon kanji, mechanical wireframes, cityscape silhouettes",
            "mood": "Dystopian, High-tech, Edgy",
            "lighting": "Neon city night glow"
        },
        "cottagecore": {
            "style": "Vintage Botanical",
            "palette": ["#8F9779", "#D2B48C", "#FFFDD0", "#556B2F"], # Sage, Tan, Cream, Olive
            "elements": "wildflowers, mushroom illustrations, hand-drawn herbs, soft linen textures",
            "mood": "Peaceful, Rustic, Whimsical",
            "lighting": "Soft golden hour sunlight"
        },
        "streetwear": {
            "style": "Modern Streetwear",
            "palette": ["#1A1A1A", "#FFFFFF", "#FF3300", "#4A4A4A"],
            "elements": "bold oversized typography, graffiti tags, industrial label layouts, distressed fabric",
            "mood": "Rebellious, Bold, Urban",
            "lighting": "High contrast studio hard light"
        },
        "vaporwave": {
            "style": "Vaporwave Aesthetic",
            "palette": ["#FF71CE", "#01CDFE", "#05FFA1", "#B967FF"], # Neon Pastel
            "elements": "classical statues, windows 95 UI, palm trees, checkerboard horizons",
            "mood": "Surreal, Chill, Retro",
            "lighting": "Neon pastel gradient wash"
        },
        "gothic": {
            "style": "Dark Gothic",
            "palette": ["#000000", "#2C2C2C", "#8B0000", "#FFFFFF"],
            "elements": "skeletal anatomy, old english fonts, ornate filigree, moon phases",
            "mood": "Dark, Mysterious, Occult",
            "lighting": "Dim moody candlelight"
        }
    }

    # Fallback for unknown keywords
    GENERIC_STYLES = [
        {
            "style": "Modern Minimalist",
            "palette": ["#000000", "#FFFFFF", "#808080"],
            "elements": "geometric shapes, sans-serif typography, clean lines"
        },
        {
            "style": "Abstract Art",
            "palette": ["#FF5733", "#33FF57", "#3357FF"],
            "elements": "fluid organic shapes, splatter textures, brush strokes"
        }
    ]

    def synthesize_design(self, keyword: str) -> Dict[str, Any]:
        """
        Takes a trend keyword and 'hallucinates' a complete design specification.
        """
        keyword_lower = keyword.lower()
        
        # 1. Knowledge Retrieval (Simulated LLM)
        knowledge = self._find_best_match(keyword_lower)
        
        # 2. Design Synthesis
        design_spec = {
            "keyword": keyword,
            "style": knowledge["style"],
            "palette": knowledge["palette"], # List of hex codes
            "palette_str": ", ".join(knowledge["palette"]), # String for prompt
            "elements": knowledge["elements"],
            "mood": knowledge.get("mood", "Trendy"),
            "lighting": knowledge.get("lighting", "Professional studio lighting")
        }
        
        # 3. Prompt Engineering (Internal)
        # We construct the prompt here to ensure the Director controls the output
        design_spec["prompt"] = self._construct_prompt(design_spec)
        
        return design_spec

    def _find_best_match(self, keyword: str) -> Dict[str, Any]:
        # Exact/Partial match in KB
        for k, v in self.STYLE_KNOWLEDGE_BASE.items():
            if k in keyword or keyword in k:
                return v
        
        # Fallback: Generate something plausible
        base = random.choice(self.GENERIC_STYLES)
        return {
            "style": f"{keyword.capitalize()} Inspired {base['style']}",
            "palette": base["palette"],
            "elements": f"{base['elements']} mingled with {keyword} motifs",
            "mood": "Creative",
            "lighting": "Balanced neutral light"
        }

    def _construct_prompt(self, spec: Dict[str, Any]) -> str:
        """
        Builds a Midjourney/SDXL optimized prompt.
        Format: [Subject] [Style] [Details] [Context] [Tech Params]
        """
        return (
            f"T-shirt design graphic, {spec['keyword']} theme, {spec['style']} style, "
            f"featuring {spec['elements']}, "
            f"color palette: {spec['palette_str']}, "
            f"{spec['mood']} atmosphere, {spec['lighting']}, "
            "vector art, high definition, detailed texture, isolated on white background, no mockup, flat 2d --v 6.0"
        )

if __name__ == "__main__":
    director = CreativeDirectorAgent()
    print(director.synthesize_design("Y2K"))
    print(director.synthesize_design("UnknownTrend"))
