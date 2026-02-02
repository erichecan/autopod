import requests
import time
import json

API_KEY = "AIzaSyBYMj9QrjHPaGi4aWQMctMykV3N3XUNaGw"
MODEL_NAME = "models/veo-3.1-fast-generate-preview"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:predict"

def generate_video():
    url = f"{BASE_URL}?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # Try Vertex-style 'instances' payload
    payload = {
        "instances": [
            {
                "prompt": "Cinematic shot of a cute cat jumping in slow motion, 4k, high quality."
            }
        ],
        "parameters": {
            "sampleCount": 1
        }
    }
    
    print(f"Sending request to {MODEL_NAME}...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    generate_video()
