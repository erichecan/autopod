# Implementation Plan - "AI Employee" Design Generator

This plan outlines the technical architecture for building the automated T-shirt design system, addressing the requirements for configurability, prompt engineering logic, and video generation.

## User Review Required
> [!IMPORTANT]
> **Video Generation API**: Direct API access to "Sora 2" or "Nanobanana" may be limited or require specific enterprise access. The implementation will use a **Adapter Pattern** to allow swapping providers (e.g., using RunwayML or Stable Video Diffusion as fallbacks if primary APIs are unavailable).

## Proposed Architecture

### Core Components
1.  **Trend Engine (Scraper)**: A modular scraper system driven by a `sources.json` configuration config.
2.  **Brain (LLM Agent)**: Analyzes trends and upgrades prompts using a strict template system.
3.  **Creative Studio (Asset Gen)**: Async pipeline for Image Generation (Midjourney/DALL-E) and Video Generation (Nanobanana).
4.  **Distribution Bot**: Handles Etsy uploads.

### File Structure
```text
/server
  /config
    sources.json        # Configurable trend sources
  /agents
    trend_scraper.py    # Fetches data based on config
    idea_analyst.py     # LLM logic for JSON attribute extraction
    prompt_engineer.py  # Template engine for upgradng prompts
  /services
    image_gen.py        # DALL-E/Midjourney Adapter
    video_gen.py        # Nanobanana/Sora Adapter
  /api
    routes.py           # Endpoints for UI to trigger jobs
```

## Proposed Changes

### [NEW] Configuration Layer
#### [NEW] `server/config/sources.json`
Defines the configurable inputs for the Trend Engine.
```json
{
  "sources": [
    { "type": "google_search", "query": "streetwear trends 2025", "frequency": "daily" },
    { "type": "pinterest", "board": "techwear-aesthetic", "limit": 10 }
  ]
}
```

### [NEW] Analysis & Prompt Engine
#### [NEW] `server/agents/prompt_engineer.py`
A class that implements the "Attribute to Prompt" logic.
```python
class PromptBuilder:
    TEMPLATE = "{lighting} of a {style} t-shirt featuring {theme} graphics, {element} details, {color} scheme, {mood} atmosphere --v 6.0"
    
    def build(self, attributes: dict) -> str:
        # Transforms JSON attributes into the final prompt string
        return self.TEMPLATE.format(**attributes)
```

### [NEW] Video Generation Pipeline
#### [NEW] `server/services/video_gen.py`
Implements the connection to Nanobanana/Sora for TikTok-ready videos.
*   **Input**: URL of the generated T-shirt mockup.
*   **Logic**:
    1.  Generate a "Motion Prompt" based on the T-shirt vibe (e.g., "Cyberpunk" -> "Neon fickering lights, slow camera pan").
    2.  Send Image + Motion Prompt to Video API.
    3.  Poll for completion.
*   **Output**: MP4 URL.

## Verification Plan

### Automated Tests
*   **Prompt Logic**: Unit tests for `PromptBuilder` to ensure attributes are correctly inserted into the template.
*   **Config Validation**: Test to verify `sources.json` can be parsed and valid scrapers are initialized.

### Manual Verification
1.  **Trend Test**: Run the scraper with a mock source and verify it produces raw trend data.
2.  **Flow Test**: Input a sample "Trend Object", run it through `idea_analyst` -> `prompt_engineer`, and verify the output prompt matches the expected formula.
3.  **Video Test**: Manually trigger the mock video service with a test image and verify it returns a valid (or mocked) video URL.
