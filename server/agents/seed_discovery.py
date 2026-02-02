import json
import random
import os
from typing import List, Dict, Any

class SeedDiscoveryAgent:
    """
    Agent responsible for managing the "Visual Trend Hunter" keyword pipeline.
    It loads seed keywords, simulates fetching trending data, and prioritizes
    terms for visual exploration.
    """
    
    def __init__(self, seed_file_path: str = "server/data/seed_keywords.json"):
        self.seed_file_path = seed_file_path
        self.seeds = self._load_seeds()
        self.active_harvest = []

    def _load_seeds(self) -> Dict[str, List[str]]:
        """Loads the base keyword library from PostgreSQL."""
        import psycopg2
        
        DB_URL = "postgresql://neondb_owner:npg_G1ExPZaM4Svw@ep-patient-dawn-ah4w5ax5-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
        seeds = {}
        
        try:
            conn = psycopg2.connect(DB_URL)
            cur = conn.cursor()
            
            cur.execute("SELECT category, keyword FROM seed_keywords WHERE is_active = TRUE")
            rows = cur.fetchall()
            
            for category, keyword in rows:
                if category not in seeds:
                    seeds[category] = []
                seeds[category].append(keyword)
                
            cur.close()
            conn.close()
            return seeds
            
        except Exception as e:
            print(f"[SeedAgent] Database Error: {e}")
            # Fallback to local JSON if DB fails (Safety net)
            return self._load_seeds_from_json()

    def _load_seeds_from_json(self):
         try:
            # Handle both absolute and relative paths for robustness
            if not os.path.exists(self.seed_file_path):
                self.seed_file_path = os.path.join(os.getcwd(), self.seed_file_path)
            
            with open(self.seed_file_path, 'r') as f:
                data = json.load(f)
                return data.get("categories", {})
         except:
             return {}

    def fetch_daily_trends(self) -> List[Dict[str, Any]]:
        """
        Simulates the "Harvest" phase:
        1. Picks random terms from different categories (simulating social chatter).
        2. Assigns a 'trend_score' (simulating Google Trends data).
        
        Returns: A prioritized list of Search Tasks.
        """
        harvested = []
        
        # Strategy: Mix of specific styles, colors, and patterns
        # In V4, this would be real API calls to Google Trends / Reddit
        
        # 1. Select a few "Hot" styles
        styles = random.sample(self.seeds.get("core_style", []), 3)
        colors = random.sample(self.seeds.get("colors_trend", []), 2)
        patterns = random.sample(self.seeds.get("patterns", []), 2)
        
        # 2. Create Search Queries combining terms for better specificity
        # e.g., "y2k aesthetic neon green"
        
        # Add single keywords
        for term in styles + colors + patterns:
            harvested.append({
                "keyword": term,
                "query": f"{term} fashion trend",
                "source": "simulated_social",
                "trend_score": round(random.uniform(0.7, 0.99), 2),
                "category": "core"
            })
            
        # Add combo keywords (Higher value)
        if styles and colors:
            combo = f"{styles[0]} {colors[0]}"
            harvested.append({
                "keyword": combo,
                "query": f"{combo} outfit",
                "source": "simulated_combo",
                "trend_score": round(random.uniform(0.85, 0.98), 2),
                "category": "combo"
            })

        # Sort by score descending
        self.active_harvest = sorted(harvested, key=lambda x: x['trend_score'], reverse=True)
        return self.active_harvest

    def get_top_tasks(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Returns the top N keywords to send to the Visual Explorer."""
        if not self.active_harvest:
            self.fetch_daily_trends()
        return self.active_harvest[:limit]

# Integration testing
if __name__ == "__main__":
    agent = SeedDiscoveryAgent()
    print(f"Loaded Categories: {agent.seeds.keys()}")
    
    print("\n--- Running Daily Harvest ---")
    tasks = agent.fetch_daily_trends()
    for t in tasks:
        print(f"[{t['trend_score']}] {t['query']} ({t['source']})")
        
    print(f"\nTop 3 for Exploration: {[t['query'] for t in agent.get_top_tasks(3)]}")
