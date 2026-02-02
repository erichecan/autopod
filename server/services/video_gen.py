import time
import uuid
import asyncio
from typing import Dict, Any

class SoraService:
    """
    Adapter for Sora 2 Video Generation API.
    """
    
    def __init__(self):
        # In-memory job store
        self.jobs: Dict[str, Dict[str, Any]] = {}

    async def start_generation(self, image_url: str, prompt: str) -> str:
        """
        Starts an async background job for Sora 2 video generation.
        """
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "status": "pending", 
            "progress": 0, 
            "url": None,
            "base_image": image_url,
            "prompt": prompt
        }
        
        asyncio.create_task(self._process_job(job_id))
        return job_id

    async def _process_job(self, job_id: str):
        print(f"[Sora2] Starting Job {job_id}...")
        self.jobs[job_id]["status"] = "processing"
        
        # Simulate Sora 2 inference (Computationally expensive)
        for i in range(0, 100, 10):
            self.jobs[job_id]["progress"] = i
            await asyncio.sleep(0.8)
            
        # Success
        # Using User-Provided Fashion Runway Reference (High Fidelity)
        # Reference: https://videos.pexels.com/video-files/5899702/5899702-uhd_4096_2160_30fps.mp4
        mock_url = "https://videos.pexels.com/video-files/5899702/5899702-uhd_4096_2160_30fps.mp4" 
        
        self.jobs[job_id]["status"] = "completed"
        self.jobs[job_id]["progress"] = 100
        self.jobs[job_id]["url"] = mock_url
        print(f"[Sora2] Job {job_id} Completed. Video: {mock_url}")

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        return self.jobs.get(job_id, {"status": "not_found"})

    def create_motion_prompt(self, attrs: dict) -> str:
        return f"Fashion runway walk, male model, front and side profiles, {attrs.get('mood', 'stylish')} atmosphere."
