import os
import requests
from server.services.image_gen import ImageGenService

def download_samples():
    service = ImageGenService()
    output_dir = "server/static/comparison"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    styles = {
        "cottagecore": "Cottagecore Botanical Nature",
        "cyberpunk": "Cyberpunk Neon Tech",
        "minimalist": "Minimalist Typography"
    }

    print("Downloading samples...")
    for name, keywords in styles.items():
        # Get one URL
        urls = service.generate_batch(keywords, count=1)
        if urls:
            url = urls[0]
            print(f"Downloading {name} from {url}...")
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    path = os.path.join(output_dir, f"{name}_sample.png")
                    with open(path, "wb") as f:
                        f.write(resp.content)
                    print(f"Saved: {path}")
            except Exception as e:
                print(f"Failed to download {name}: {e}")

if __name__ == "__main__":
    download_samples()
