import requests
import time
import json
import os

API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
MODEL_NAME = "models/veo-3.1-fast-generate-preview"
URL_LRO = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:predictLongRunning"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# The Prompt we decided on in routes.py
PROMPT = (
    "Models on a Fashion Runway. "
    "A stylish man walking forward wearing a white t-shirt with an abstract colorful bubble pattern (pink, blue, yellow) on the chest. "
    "Runway Walk motion. "
    "Ensure the Design Asset is visible. "
    "Photorealistic, 4k, cinematic lighting. Duration: 15s."
)

def generate_demo():
    print(f"1. Starting Generation with Prompt:\n'{PROMPT}'\n")
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "instances": [{"prompt": PROMPT}],
        "parameters": {"sampleCount": 1}
    }
    
    url = f"{URL_LRO}?key={API_KEY}"
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
                save_path = f"{save_dir}/final_veo_runway.mp4"
                
                print(f"Downloading to {save_path}...")
                
                # Appending Key is CRITICAL for generativelanguage.googleapis.com downloads
                download_url = uri
                if "key=" not in uri:
                    download_url = f"{uri}&key={API_KEY}"
                    
                vid_resp = requests.get(download_url)
                with open(save_path, "wb") as f:
                    f.write(vid_resp.content)
                    
                print(f"SUCCESS. File saved at: {os.path.abspath(save_path)}")
                break
            else:
                print(".", end="", flush=True)
                
    except Exception as e:
        print(f"\nException: {e}")

if __name__ == "__main__":
    generate_demo()
