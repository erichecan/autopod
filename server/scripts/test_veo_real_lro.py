import requests
import time
import json

API_KEY = "AIzaSyBYMj9QrjHPaGi4aWQMctMykV3N3XUNaGw"
MODEL_NAME = "models/veo-3.1-fast-generate-preview"
URL_LRO = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:predictLongRunning"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

def generate_and_poll():
    # 1. Start Generation
    print(f"1. Starting generation job at {URL_LRO}...")
    headers = {"Content-Type": "application/json"}
    payload = {
        "instances": [
             # Simple prompt for verification
            {"prompt": "A futuristic chrome drone flying through a cyberpunk city, neon lights, 4k, photorealistic."}
        ],
        "parameters": {
            "sampleCount": 1
        }
    }
    
    url = f"{URL_LRO}?key={API_KEY}"
    try:
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            print(f"Start Failed: {resp.status_code} - {resp.text}")
            return
            
        data = resp.json()
        print("Job Started!")
        print(json.dumps(data, indent=2))
        
        # Extract Operation Name
        # Check standard LRO response keys
        op_name = data.get("name") # "operations/..."
        if not op_name:
            print("No operation name found.")
            return
            
        # 2. Poll Status
        print(f"\n2. Polling Operation: {op_name}")
        while True:
            poll_url = f"{BASE_URL}/{op_name}?key={API_KEY}"
            poll_resp = requests.get(poll_url)
            
            if poll_resp.status_code != 200:
                print(f"Poll Error: {poll_resp.status_code}")
                break
                
            poll_data = poll_resp.json()
            done = poll_data.get("done", False)
            
            if done:
                print("\nJob Done!")
                print(json.dumps(poll_data, indent=2))
                # Check for response video
                if "response" in poll_data:
                     print("\nVIDEO GENERATED SUCCESSFULLY.")
                elif "error" in poll_data:
                     print("\nGENERATION FAILED.")
                break
            else:
                print(".", end="", flush=True)
                time.sleep(3)
                
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    generate_and_poll()
