from typing import Dict, Any

class PromptBuilder:
    """
    Transforms structured design attributes into high-quality image generation prompts.
    """
    
    # Template based on requirement: [Photography/Medium] of a [Style] t-shirt featuring [Theme] graphics...
    TEMPLATE = (
        "{lighting} of a {style} t-shirt featuring {theme} graphics, "
        "{elements} details, {colors} scheme, {mood} atmosphere --v {version}"
    )

    DEFAULTS = {
        "lighting": "Professional product photography",
        "style": "classic fit",
        "theme": "modern",
        "elements": "minimalist",
        "colors": "black and white",
        "mood": "clean",
        "version": "6.0"
    }

    def build(self, attributes: Dict[str, Any]) -> str:
        """
        Constructs the final prompt string by merging input attributes with defaults.
        """
        # Merge defaults with provided attributes
        data = self.DEFAULTS.copy()
        data.update(attributes)
        
        # Format the template
        return self.TEMPLATE.format(**data)

if __name__ == "__main__":
    # Test
    builder = PromptBuilder()
    test_attrs = {
        "style": "Boxy fit",
        "theme": "Cyberpunk Utility",
        "elements": "Kanji typography and electric circuit patterns",
        "colors": "Matte black base with neon amber highlights",
        "mood": "Edgy dramatic"
    }
    print(builder.build(test_attrs))
