import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from server.services.compositor import CompositorService

# Paths from Artifacts (Absolute)
DESIGN_PATH = "/Users/eric/.gemini/antigravity/brain/7791c775-bb52-4547-8010-6243cbca6b36/design_neon_1769926529446.png"
MODEL_PATH = "/Users/eric/.gemini/antigravity/brain/7791c775-bb52-4547-8010-6243cbca6b36/white_tshirt_mockup_1769919198298.png"

# Output
OUTPUT_DIR = "/Users/eric/.gemini/antigravity/brain/7791c775-bb52-4547-8010-6243cbca6b36"
OUTPUT_FILENAME = "vton_neon_strict.png"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

def run_strict_vton():
    print(f"1. Loading Design: {DESIGN_PATH}")
    print(f"2. Loading Base Model: {MODEL_PATH}")
    
    service = CompositorService()
    try:
        final_path = service.composite_design(
            design_path=DESIGN_PATH, 
            model_path=MODEL_PATH, 
            output_path=OUTPUT_PATH
        )
        print(f"SUCCESS: Strict VTON Image saved at: {final_path}")
    except Exception as e:
        print(f"FAILURE: {e}")

if __name__ == "__main__":
    run_strict_vton()
