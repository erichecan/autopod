import json
import random
from pathlib import Path
from typing import List, Dict, Any

class TrendScraper:
    def __init__(self, config_path: str = "server/config/sources.json"):
        self.config_path = Path(config_path)
        self.sources = self._load_config()

    def _load_config(self) -> List[Dict[str, Any]]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            data = json.load(f)
            return data.get("sources", [])

    def fetch_trends(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetches trend data from the high-fidelity mock library.
        Randomly samples items to simulate live updates.
        """
        mock_data_path = Path("server/data/mock_trends.json")
        if not mock_data_path.exists():
            return {"error": "Mock data missing"}
            
        with open(mock_data_path, 'r') as f:
            all_trends = json.load(f)
            
        results = {
            "google_search": random.sample(all_trends.get("google_search", []), 3),
            "pinterest": random.sample(all_trends.get("pinterest", []), 3),
            "instagram": random.sample(all_trends.get("instagram", []), 3)
        }
        
        return results

    def _mock_google_search(self, config: Dict) -> List[Dict]:
        return [] # Deprecated

    def _mock_pinterest(self, config: Dict) -> List[Dict]:
        return [] # Deprecated

    def _mock_instagram(self, config: Dict) -> List[Dict]:
        return [] # Deprecated

if __name__ == "__main__":
    # Test run
    scraper = TrendScraper("server/config/sources.json")
    trends = scraper.fetch_trends()
    print(json.dumps(trends, indent=2))
