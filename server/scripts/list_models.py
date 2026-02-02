import requests

API_KEY = "AIzaSyBYMj9QrjHPaGi4aWQMctMykV3N3XUNaGw"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def list_models():
    url = f"{BASE_URL}?key={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("Available Models:")
            for m in models:
                if 'video' in m['name'] or 'veo' in m['name']:
                    print(f" - {m['name']}")
            print(f"\nTotal models found: {len(models)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    list_models()
