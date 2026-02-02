import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from server.agents.trend_scraper import TrendScraper
from server.agents.creative_director import CreativeDirectorAgent
from server.agents.prompt_engineer import PromptBuilder
from server.services.veo import VeoService

# ... (Imports)

router = APIRouter()

# Services (Singletons)
scraper = TrendScraper("server/config/sources.json")
director = CreativeDirectorAgent()
prompt_builder = PromptBuilder()
# Using the API Key provided by env
veo_service = VeoService()
image_service = ImageGenService()
seed_agent = SeedDiscoveryAgent()
explorer_agent = VisualExplorerAgent()
mockup_engine = MockupEngine() # Legacy
nano_banana = NanoBananaService() # New High Fidelity VTON

# ... (Routes)

@router.post("/generate-video")
async def generate_video(request: VideoRequest):
    """
    (DISABLED) Starts a Veo 3.1 video job.
    Disabled to save costs ($2.25/video). Focus on VTON Images only.
    """
    return {"status": "skipped", "message": "Video generation is currently disabled for cost optimization. Please use VTON images."}
    # try:
    #     # Prompt Logic: Image-to-Video (Visuals Reference)
    #     # We now provide the VTON image directly to Veo.
    #     motion_prompt = (
    #         "Cinematic Runway Walk. "
    #         "Bring this fashion model to life. "
    #         "The model executes a confident runway walk forward. "
    #         "The customized t-shirt design (abstract colorful bubbles) must remain stable and clearly visible on the chest. "
    #         "Photorealistic, 4k, cinematic lighting. Duration: 15s."
    #     )
    #     # Ensure we are passing the local path if possible, or handling the URL correctly in service
    #     # For this demo, we assume image_url is the local path or accessible
    #     job_id = await veo_service.start_generation(request.image_url, motion_prompt)
    #     return {"job_id": job_id, "status": "pending"}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    status = veo_service.get_job_status(job_id)
    if status["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    return status
