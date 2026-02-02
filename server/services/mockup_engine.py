import os
import requests
from io import BytesIO
from PIL import Image

class MockupEngine:
    """
    Composites a design image onto a T-Shirt blank.
    """
    
    def __init__(self, base_image_path: str = "white_tshirt_mockup_1769919198298.png"):
        # Expecting the base image to be in the artifacts folder or passed in
        # For this setup, we'll look in the same directory or static folder
        self.base_path = base_image_path
        self.output_dir = "server/static/mockups"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_mockup(self, design_url: str) -> str:
        """
        Overlays the design from the URL onto the center of the T-shirt.
        Returns the local path (URL) of the result.
        """
        try:
            # 1. Load Base T-Shirt
            # If absolute path, use it. If relative, try to find it.
            # Assuming the generated asset is in the brain dir, we need its absolute path or copy it.
            # For simplicity in this demo, strict path handling might be needed.
            # I will assume the base image is available. If not, I'll use a placeholder or error out.
            
            if os.path.exists(self.base_path):
                base = Image.open(self.base_path).convert("RGBA")
            elif os.path.exists(f"/Users/eric/.gemini/antigravity/brain/7791c775-bb52-4547-8010-6243cbca6b36/{self.base_path}"):
                 base = Image.open(f"/Users/eric/.gemini/antigravity/brain/7791c775-bb52-4547-8010-6243cbca6b36/{self.base_path}").convert("RGBA")
            else:
                # Create a blank white canvas if base missing
                print(f"[MockupEngine] Base image not found at {self.base_path}, creating blank.")
                base = Image.new("RGBA", (800, 800), (240, 240, 240, 255))

            # 2. Download Design Image
            response = requests.get(design_url)
            response.raise_for_status()
            design = Image.open(BytesIO(response.content)).convert("RGBA")

            # 3. Resize and Position Design
            # Center the design approx 30% width of the shirt
            shirt_width, shirt_height = base.size
            target_width = int(shirt_width * 0.35)
            aspect_ratio = design.height / design.width
            target_height = int(target_width * aspect_ratio)
            
            design = design.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Position: Center X, ~25% from Top Y (standard chest placement)
            x_pos = (shirt_width - target_width) // 2
            y_pos = int(shirt_height * 0.25)
            
            # 4. Composite
            # Use the design as a paste (with transparency if exists)
            base.paste(design, (x_pos, y_pos), design)
            
            # 5. Save
            # Filename based on design URL hash or timestamp
            filename = f"mockup_{abs(hash(design_url))}.png"
            save_path = os.path.join(self.output_dir, filename)
            base.save(save_path)
            
            return f"/static/mockups/{filename}"

        except Exception as e:
            print(f"[MockupEngine] Error: {e}")
            return "/static/error_mockup.png"
