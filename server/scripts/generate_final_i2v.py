import requests
import time
import json
import base64
import os

API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
MODEL_NAME = "models/veo-3.1-fast-generate-preview"
URL_LRO = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:predictLongRunning"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# The VTON Result from the Walkthrough
VTON_IMAGE_PATH = "/Users/eric/.gemini/antigravity/brain/7791c775-bb52-4547-8010-6243cbca6b36/vton_man_wearing_design_1769921893861.png"

PROMPT = (
    "Cinematic Runway Walk. "
    "Bring this fashion model to life. "
    "The model executes a confident runway walk forward. "
    "The customized t-shirt design (abstract colorful bubbles) must remain stable and clearly visible on the chest. "
    "Photorealistic, 4k, cinematic lighting. Duration: 15s."
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_final_i2v():
    print(f"1. Encoding VTON Image: {VTON_IMAGE_PATH}")
    if not os.path.exists(VTON_IMAGE_PATH):
        print("Image file not found!")
        return

    b64_image = encode_image(VTON_IMAGE_PATH)
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "instances": [
            {
                "prompt": PROMPT,
                "image": {
                    "bytesBase64Encoded": b64_image,
                    "mimeType": "image/png"
                }
            }
        ],
        "parameters": {
            "sampleCount": 1
        }
    }
    
    url = f"{URL_LRO}?key={API_KEY}"
    print(f"2. Sending I2V Request to Veo 3.1...")
    
    try:
        # Start
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            print(f"Error Starting: {resp.text}")
            return
            
        data = resp.json()
        op_name = data.get("name")
        print(f"Job Started. Operation: {op_name}")
        
        # Poll
        print("Polling...", end="", flush=True)
        while True:
            time.sleep(5)
            poll_resp = requests.get(f"{BASE_URL}/{op_name}?key={API_KEY}")
            poll_data = poll_resp.json()
            
            if poll_data.get("done"):
                if "error" in poll_data:
                    print(f"\nFailed: {poll_data['error']}")
                    return
                
                # Get URI
                uri = poll_data["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                print(f"\nVideo Generated! URI: {uri}")
                
                # Download
                save_dir = "server/static/generated"
                os.makedirs(save_dir, exist_ok=True)
                save_path = f"{save_dir}/final_veo_i2v_runway.mp4"
                
                print(f"Downloading to {save_path}...")
                
                # Key append logic
                download_url = uri
                if "key=" not in uri:
                    download_url = f"{uri}&key={API_KEY}"
                    
                vid_resp = requests.get(download_url)
                if vid_resp.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(vid_resp.content)
                    print(f"SUCCESS. File saved at: {os.path.abspath(save_path)}")
                else:
                    print(f"Download Failed: {vid_resp.status_code}")
                    print(vid_resp.text)
                break
            else:
                print(".", end="", flush=True)
                
    except Exception as e:
        print(f"\nException: {e}")

if __name__ == "__main__":
    generate_final_i2v()
