import requests
import time
import json
import base64
import os

API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
MODEL_NAME = "models/veo-3.1-fast-generate-preview"
URL_LRO = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:predictLongRunning"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Path to the VTON image (using one from artifacts for testing)
# Note: In production this comes from the NanoBanana service result
VTON_IMAGE_PATH = "/Users/eric/.gemini/antigravity/brain/7791c775-bb52-4547-8010-6243cbca6b36/vton_man_wearing_design_1769921893861.png"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_i2v():
    print(f"1. Encoding Image: {VTON_IMAGE_PATH}")
    if not os.path.exists(VTON_IMAGE_PATH):
        print("Image file not found!")
        return

    b64_image = encode_image(VTON_IMAGE_PATH)
    
    headers = {"Content-Type": "application/json"}
    
    # Vertex AI / Gemini API Multimodal Payload for Veo
    # Hypothesis: Standard "image" field in instances
    payload = {
        "instances": [
            {
                "prompt": "Cinematic drone shot of this man walking, showing the design on his shirt clearly. 4k.",
                "image": {
                    "bytesBase64Encoded": b64_image,
                    "mimeType": "image/png"  # Explicitly stating mimeType helps sometimes
                }
            }
        ],
        "parameters": {
            "sampleCount": 1
        }
    }
    
    url = f"{URL_LRO}?key={API_KEY}"
    print(f"2. Sending Request to {URL_LRO}...")
    
    try:
        resp = requests.post(url, headers=headers, json=payload)
        
        if resp.status_code != 200:
            print(f"Start Failed: {resp.status_code}")
            print(resp.text)
            return
            
        data = resp.json()
        print("Job Started!")
        print(json.dumps(data, indent=2))
        
        # We don't need to poll for this test, just want to see if it ACCEPTS the image
        op_name = data.get("name")
        if op_name:
            print(f"SUCCESS: Image accepted. Operation: {op_name}")
        else:
            print("WARNING: No operation name, but 200 OK?")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    generate_i2v()
