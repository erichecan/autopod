import time

class ImageGenService:
    """
    Service to generate T-Shirt mockups from prompts.
    Uses Async batching in production (DALL-E/Midjourney).
    Here uses Mock data.
    """
    
    def generate_batch(self, prompt: str, count: int = 10) -> list[str]:
        """
        Generates a batch of image URLs.
        Uses Smart Mocking: extracting keywords from prompt to fetch relevant Unsplash images.
        """
        print(f"[ImageGen] Generating {count} images for prompt: {prompt[:50]}...")
        time.sleep(1)
        
        # Simple extraction of viable keywords for search
        keywords = "t-shirt,pattern"
        if "Neon" in prompt or "Cyber" in prompt:
            keywords = "neon,cyberpunk,digital+art"
        elif "Nature" in prompt or "Botanical" in prompt:
            keywords = "leaves,botanical,illustration"
        elif "Retro" in prompt or "90s" in prompt:
            keywords = "retro,80s,synthwave"
        elif "Minimalist" in prompt:
            keywords = "minimalist,typography,abstract"
            
        results = []
        for i in range(count):
            # Use Unsplash Source with specific keywords and a random seed sig parameter to ensure variety
            # We use 'random' endpoint which redirects to a real image
            # Adding a size of 400x400 for consistency
            seed = int(time.time() * 1000) + i
            url = f"https://images.unsplash.com/photo-{1500000000000+i}?w=400&h=400&fit=crop&q=80" # Fallback setup
            
            # Using Unsplash source API format for correct keyword search
            # Format: https://source.unsplash.com/random/400x400/?keyword1,keyword2&sig=123
            # Note: source.unsplash.com is deprecated/unreliable, better to use direct search-like random URLs if possible
            # or simulate by rotating a hardcoded realistic list if API access isn't available.
            # For this "High Fidelity Mock", let's use a trick:
            # We append a random query param to a set of KNOWN good URLs based on category to ensure they load.
            
            base_url = self._get_base_url_for_style(keywords, i)
            results.append(base_url)
            
        print(f"[ImageGen] Completed batch generation.")
        return results

    def _get_base_url_for_style(self, keywords: str, index: int) -> str:
        # Curated list of high-quality Unsplash IDs for reliability
        collections = {
            "neon": ["1550684848-fac1c5b4e853", "1617391764619-35a0ce0d96d9", "1563089145-599997674d42"],
            "botanical": ["1518556622415-g24528148332", "1477414348463-c0eb7f1359b6", "1507722718-2029729a6565"],
            "retro": ["1578632292335-df3abbb0d586", "1574180566232-a8465d31405c", "1605218427306-0b62e49c71df"],
            "minimalist": ["1503342394128-c104d54dba01", "1494438639946-1ebd1d20bf85", "1507679721510-33b6dd228e7e"]
        }
        
        # Determine category
        category = "minimalist"
        if "neon" in keywords: category = "neon"
        elif "botanical" in keywords: category = "botanical"
        elif "retro" in keywords: category = "retro"
        
        # Pick Image ID
        ids = collections.get(category, collections["minimalist"])
        img_id = ids[index % len(ids)]
        
        return f"https://images.unsplash.com/photo-{img_id}?w=400&h=400&fit=crop&q=80"
