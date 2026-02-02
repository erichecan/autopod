import sys
import os

# Add server directory to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from server.agents.trend_scraper import TrendScraper
from server.agents.idea_analyst import IdeaAnalyst
from server.agents.prompt_engineer import PromptBuilder
from server.services.video_gen import VideoGenService

def run_pipeline():
    print("=== STARTING AI EMPLOYEE PIPELINE ===")
    
    # 1. Fetch Trends
    print("\n--- PHASE 1: MARKET RESEARCH ---")
    scraper = TrendScraper("server/config/sources.json")
    trends = scraper.fetch_trends()
    print(f"Fetched {len(trends)} trends.")
    if not trends:
        print("No trends found. Exiting.")
        return
    
    # Pick one trend for demo
    selected_trend = trends[0]
    print(f"Selected Trend: {selected_trend['description']}")

    # 2. Analyze Trend
    print("\n--- PHASE 2: AI ANALYSIS ---")
    analyst = IdeaAnalyst()
    attributes = analyst.analyze(selected_trend)
    print("Extracted Attributes:")
    for k, v in attributes.items():
        print(f"  {k}: {v}")

    # 3. Build Prompt
    print("\n--- PHASE 3: PROMPT ENGINEERING ---")
    builder = PromptBuilder()
    image_prompt = builder.build(attributes)
    print(f"Generated Image Prompt: \n  \"{image_prompt}\"")

    # 4. Generate Video Token
    print("\n--- PHASE 5: VIDEO MARKETING ---")
    video_service = VideoGenService()
    # Mocking an image URL that would come from Phase 3 (Image Gen)
    mock_image_url = "https://mock-image-gen.com/shirt_123.png"
    
    tiktok_prompt = video_service.create_tiktok_prompt(attributes)
    video_url = video_service.generate_video(mock_image_url, tiktok_prompt)
    
    print("\n=== PIPELINE COMPLETE ===")
    print(f"Final Asset: {video_url}")

if __name__ == "__main__":
    run_pipeline()
