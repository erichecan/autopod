import requests
import time
import os
API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY")
MODEL_NAME = "models/veo-3.1-fast-generate-preview"
# CHANGED: Using :generateContent instead of :predict
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent"

def generate_video():
    url = f"{BASE_URL}?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # Standard Gemini payload
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Cinematic shot of a cute cat jumping in slow motion, 4k, high quality."}
                ]
            }
        ]
    }
    
    print(f"Sending request to {url}...")
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
