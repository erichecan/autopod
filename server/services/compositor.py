from PIL import Image, ImageOps
import os

class CompositorService:
    """
    Deterministic Image Compositor to ensure exact design fidelity.
    Overlay Design (Phase 1) -> Model Base Image (Phase 2).
    """

    def __init__(self, base_model_path=None):
        # We need a fallback base model if not provided
        # I'll default to the one found in static if available, or expect it passed
        self.default_base = base_model_path

    def composite_design(self, design_path: str, model_path: str, output_path: str):
        """
        Overlay design_path onto model_path.
        Assumes model_path is a standardized Front-Facing T-shirt.
        """
        try:
            # 1. Load Images
            if not os.path.exists(design_path):
                raise FileNotFoundError(f"Design not found: {design_path}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Base Model not found: {model_path}")

            design = Image.open(design_path).convert("RGBA")
            base = Image.open(model_path).convert("RGBA")
            
            base_w, base_h = base.size
            
            # 2. Calculate Placement (Standard Chest Placement)
            # Assumption: On a standard model shot, chest is roughly centered width-wise,
            # and starts around 25-30% down the height.
            # Let's scale design to occupy ~40% of the image width
            target_width = int(base_w * 0.45)
            aspect_ratio = design.height / design.width
            target_height = int(target_width * aspect_ratio)
            
            design_resized = design.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Position: Center X, 30% Y
            pos_x = (base_w - target_width) // 2
            pos_y = int(base_h * 0.28) # 28% from top is usually chest-level for portraits
            
            # 3. Blending (Multiply Mode Simulation for Realism)
            # For strict fidelity, "Normal" paste is safest for color accuracy.
            # "Multiply" is better for folds/shadows but changes colors (Neon becomes dark).
            # The User requested "Identical" (一模一样), so we use Normal paste but maybe slightly reduced opacity if needed.
            # Actually, standard print-on-demand is vivid. Let's do Normal Overlay.
            
            # Create a transparent layer for composition
            comp_layer = Image.new('RGBA', base.size, (0,0,0,0))
            comp_layer.paste(design_resized, (pos_x, pos_y))
            
            # Composite
            final_image = Image.alpha_composite(base, comp_layer)
            
            # 4. Save
            final_image = final_image.convert("RGB") # Remove alpha for JPEG/PNG comp
            final_image.save(output_path, quality=95)
            print(f"[Compositor] Saved strict VTON result to {output_path}")
            return output_path

        except Exception as e:
            print(f"[Compositor] Error: {e}")
            raise e

if __name__ == "__main__":
    # Test Code
    service = CompositorService()
    # Dummy paths for testing if run directly
    # service.composite_design("design.png", "model.png", "output.png")
