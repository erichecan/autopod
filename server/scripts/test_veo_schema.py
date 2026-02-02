import requests
import json

API_KEY = "AIzaSyBYMj9QrjHPaGi4aWQMctMykV3N3XUNaGw"
MODEL_NAME = "models/veo-3.1-fast-generate-preview"
URL_PREDICT = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:predict"
URL_LRO = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:predictLongRunning"

def test_endpoint(name, url, payload):
    print(f"\n--- Testing {name} ---")
    full_url = f"{url}?key={API_KEY}"
    try:
        response = requests.post(full_url, headers={"Content-Type": "application/json"}, json=payload)
        print(f"Status: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
    except Exception as e:
        print(f"Ex: {e}")

if __name__ == "__main__":
    test_endpoint("PREDICT (Empty)", URL_PREDICT, {})
    test_endpoint("LRO (Empty)", URL_LRO, {})
