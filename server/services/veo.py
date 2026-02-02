import requests
import time
import uuid
import asyncio
import base64
import os
from typing import Dict, Any, Optional

class VeoService:
    """
    Adapter for Google Veo 3.1 Fast Video Generation API.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            print("[Warning] VeoService initialized without API Key. Please set GOOGLE_API_KEY env var.")
        # Correct endpoint for Veo 3.1 Fast (Preview)
        # Using Generative Language API (Gemini family)
        self.base_url_base = "https://generativelanguage.googleapis.com/v1beta"
        self.jobs: Dict[str, Dict[str, Any]] = {}

    async def start_generation(self, image_url: str, prompt: str) -> str:
        """
        Starts an async background job for Veo video generation.
        image_url: Local path or URL to the VTON image.
        """
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "status": "pending", 
            "progress": 0, 
            "url": None,
            "error": None
        }
        
        asyncio.create_task(self._process_job(job_id, image_url, prompt))
        return job_id

    async def _process_job(self, job_id: str, image_url: str, prompt: str):
        print(f"[Veo] Starting Job {job_id} with Prompt: {prompt[:50]}...")
        if image_url:
            print(f"[Veo] Using Image Input: {image_url}")
            
        self.jobs[job_id]["status"] = "processing"
        
        # Veo 3.1 Fast LRO Endpoint
        model_name = "models/veo-3.1-fast-generate-preview"
        url_lro = f"{self.base_url_base}/{model_name}:predictLongRunning?key={self.api_key}"
        
        headers = {"Content-Type": "application/json"}
        
        instance_data = {"prompt": prompt}
        
        # Add Image if provided and accessible locally
        if image_url and os.path.exists(image_url):
            try:
                with open(image_url, "rb") as f:
                    b64_img = base64.b64encode(f.read()).decode('utf-8')
                instance_data["image"] = {
                    "bytesBase64Encoded": b64_img,
                    "mimeType": "image/png" # Assuming PNG from VTON
                }
            except Exception as e:
                print(f"[Veo] Error reading image: {e}")
        
        payload = {
            "instances": [instance_data],
            "parameters": {
                "sampleCount": 1
            }
        }
        
        try:
            # 1. Start Job
            resp = requests.post(url_lro, headers=headers, json=payload)
            if resp.status_code != 200:
                raise Exception(f"API Error {resp.status_code}: {resp.text}")
            
            data = resp.json()
            op_name = data.get("name")
            if not op_name:
                raise Exception("No operation name returned")
            
            print(f"[Veo] Operation Started: {op_name}")
            
            # 2. Poll
            while True:
                time.sleep(3) # Poll interval
                poll_url = f"{self.base_url_base}/{op_name}?key={self.api_key}"
                poll_resp = requests.get(poll_url)
                
                if poll_resp.status_code != 200:
                    raise Exception(f"Poll Failed: {poll_resp.status_code}")
                
                poll_data = poll_resp.json()
                if poll_data.get("done"):
                    if "error" in poll_data:
                        raise Exception(f"Generation Failed: {poll_data['error']}")
                        
                    # 3. Extract Result
                    try:
                        uri = poll_data["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
                    except KeyError:
                         raise Exception("Video URI not found in response")
                    
                    print(f"[Veo] Video Generated: {uri}")
                    
                    # 4. Download Video (Optional but recommended for persistence)
                    # We save it to a local file
                    save_path = f"server/static/generated/veo_{job_id}.mp4"
                    # Create dir if not exists (it should from other services)
                    
                    print(f"[Veo] Downloading to {save_path}...")
                    # The URI from Gemini API is usually a download link. 
                    # If it's a file resource, it might need the Key appended if not public.
                    # Current URI seems to be: https://generativelanguage.googleapis.com/v1beta/files/...
                    # Let's try appending key if it looks like a googleapis link
                    download_url = uri
                    if "googleapis.com" in uri and "key=" not in uri:
                         download_url = f"{uri}&key={self.api_key}"

                    video_resp = requests.get(download_url)
                    
                    if video_resp.status_code == 200 and "application/json" not in video_resp.headers.get("Content-Type", ""):
                        with open(save_path, "wb") as f:
                            f.write(video_resp.content)
                        final_url = f"/static/generated/veo_{job_id}.mp4"
                        print(f"[Veo] Download Success. File saved.")
                    else:
                        print(f"[Veo] Download failed ({video_resp.status_code}).")
                        print(f"Response: {video_resp.text[:200]}")
                        # If failed, do not claim success or save file
                        raise Exception(f"Download Error {video_resp.status_code}: {video_resp.text[:200]}")
                        
                    self.jobs[job_id]["status"] = "completed"
                    self.jobs[job_id]["progress"] = 100
                    self.jobs[job_id]["url"] = final_url
                    print(f"[Veo] Job {job_id} Completed. Access at: {final_url}")
                    break
                    
        except Exception as e:
            print(f"[Veo] Job {job_id} Failed: {e}")
            self.jobs[job_id]["status"] = "failed"
            self.jobs[job_id]["error"] = str(e)

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        return self.jobs.get(job_id, {"status": "not_found"})
