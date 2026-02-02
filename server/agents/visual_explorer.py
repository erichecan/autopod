import os
import asyncio
import time
import random
from playwright.async_api import async_playwright

class VisualExplorerAgent:
    """
    Agent responsible for capturing visual evidence of trends.
    Uses Playwright (Async) to browse Bing Images and take screenshots.
    Optimized for Stealth to avoid bot detection.
    """
    
    def __init__(self, output_dir: str = "server/static/screenshots"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    async def search_and_capture(self, keyword: str, limit: int = 1) -> list[str]:
        """
        Searches Bing Images for the keyword and captures screenshots of the grid.
        Returns a list of local file paths to the screenshots.
        """
        screenshot_paths = []
        
        print(f"[VisualExplorer] Hunting visuals for: {keyword}...")
        
        try:
            async with async_playwright() as p:
                # Launch browser with arguments to look like a real user
                browser = await p.chromium.launch(
                    headless=True, # Keep headless for server
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--window-size=1920,1080',
                        '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    ]
                )
                
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                
                # Anti-detection script
                await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """)
                
                page = await context.new_page()
                
                # Navigate to Bing Image Search
                search_query = keyword.replace(" ", "+")
                search_url = f"https://www.bing.com/images/search?q={search_query}"
                print(f"[VisualExplorer] Navigating to: {search_url}")
                
                try:
                    await page.goto(search_url, wait_until="networkidle", timeout=30000)
                except Exception as e:
                    print(f"[VisualExplorer] Navigation timeout/error: {e}")
                    
                # Random delay
                await asyncio.sleep(random.uniform(2, 4))
                
                # Robust Image Search Strategy for Bing
                # 1. Wait for result images (Bing typically uses .mimg class)
                try:
                    await page.wait_for_selector('img.mimg', state='visible', timeout=15000)
                except:
                    print("[VisualExplorer] Timeout waiting for images.")
                    # Dump HTML for debugging
                    content = await page.content()
                    with open(os.path.join(self.output_dir, "debug_failure.html"), "w") as f:
                        f.write(content)
                    
                # Simulate human scrolling to trigger lazy loading
                await self._human_scroll(page)
                
                # 2. Find "Real" Result Images
                safe_keyword = keyword.replace(" ", "_").lower()
                
                captured_count = 0
                for i in range(limit):
                    filename = f"{safe_keyword}_{int(time.time())}_{i}.png"
                    path = os.path.join(self.output_dir, filename)
                    
                    # Check for visible images in viewport using 'img.mimg' selector
                    visible_images = await page.evaluate("""() => {
                        return Array.from(document.querySelectorAll('img.mimg')).filter(img => {
                            const rect = img.getBoundingClientRect();
                            return rect.width > 50 && rect.height > 50 && rect.top >= 0 && rect.top < window.innerHeight;
                        }).length;
                    }""")
                    
                    if visible_images > 0:
                        await page.screenshot(path=path, full_page=False)
                        screenshot_paths.append(path)
                        print(f"[VisualExplorer] Captured: {path} (Matches: {visible_images})")
                        captured_count += 1
                    else:
                        print(f"[VisualExplorer] Warning: No significant images found in viewport {i}")
                    
                    # Scroll down for next shot if limit > 1
                    if i < limit - 1:
                        await self._human_scroll(page, distance=800)

                if captured_count == 0:
                     print("[VisualExplorer] Warning: No valid images captured. Saving debug view.")
                     await page.screenshot(path=os.path.join(self.output_dir, "debug_view.png"))

                await browser.close()
                
            return screenshot_paths
            
        except Exception as e:
            print(f"[VisualExplorer] Error capturing {keyword}: {e}")
            return []

    async def _human_scroll(self, page, distance=None):
        """Simulates human-like scrolling behavior with pauses."""
        # total_height = await page.evaluate("document.body.scrollHeight")
        
        if distance:
            # Scroll specific distance
            steps = distance // 100
        else:
            # Scroll a bit to load lazy images
            steps = 5
            
        for _ in range(steps):
             scroll_amount = random.randint(100, 300)
             await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
             await asyncio.sleep(random.uniform(0.2, 0.8))
             
             # Randomly mouse move
             await page.mouse.move(random.randint(0, 500), random.randint(0, 500))
