# Product Specification: AI Visual Trend Hunter & Design Engine

> **Version**: 1.0  
> **Status**: DRAFT  
> **Last Updated**: 2026-01-31

## 1. Executive Summary
This system automates the creative direction process for fashion design (specifically T-shirts) by simulating a human designer's research workflow. Instead of relying on static databases, it dynamically hunts for "visual evidence" of trends across the web, analyzes screenshots to extract aesthetic features (color, pattern, style), and synthesizes these insights into high-quality AI image generation prompts.

## 2. Core Value Proposition
*   **Visual-First Intelligence**: Extracts trends directly from visual sources (images, screenshots) rather than just text statistics.
*   **Copyright-Safe Research**: Analyzes screenshots of search results (aggregates) to identify patterns without downloading or copying individual copyrighted works.
*   **Closed-Loop Automation**: From "Trend Discovery" to "Final Design Asset" without human intervention.
*   **Quantifiable Aesthetics**: Turns subjective "vibes" into objective data (HEX codes, style vectors, trend scores).

## 3. System Architecture

### 3.1 High-Level Workflow
The system follows a 6-step linear pipeline:
1.  **Seed Discovery**: Identify "what to look for" (Hot Keywords).
2.  **Visual Exploration**: Batch search & screenshot "proof" of trends (Google Images).
3.  **Visual Analysis**: Extract raw visual data (Colors, Patterns, Styles) from screenshots.
4.  **Trend Synthesis**: Combine quantitative visual data with semantic trend logic.
5.  **Prompt Engineering**: Construct platform-optimized prompts (Midjourney/SD).
6.  **Asset Generation**: Generate and publish final designs.

---

## 4. Functional Modules

### 4.1 Module A: Trend Seed Discovery Engine
**Goal**: Maintain a dynamic, self-updating library of 100+ "Seed Keywords" (e.g., *Y2K, Cottagecore, Streetwear*).

*   **Data Sources & Frequency**:
    *   **Daily**: Social Media (TikTok/IG hashtags), Retail Bestsellers (Shein/Zara).
    *   **Weekly**: Search Trends (Google/Pinterest Trends), Design Communities (Behance).
    *   **Quarterly**: Industry Reports (Vogue/WGSN/Pantone).
*   **Keyword Scoring Model**:
    *   `Trend Score (0-1)`: Based on search curve slope.
    *   `Longevity Score (0-1)`: How long it has been active.
    *   `Versatility Score (0-1)`: Frequency of co-occurrence with other descriptors.
    *   **Lifecycle Management**: Auto-archive keywords with <0 search volume for 8 weeks; "Hall of Fame" for classics (Vintage, Minimalist).

### 4.2 Module B: Visual Intelligence Engine (The "Eyes")
**Goal**: Simulate a designer browsing the web and spotting patterns.

*   **Browsing & Capture**:
    *   **Technique**: Headless browsing (Puppeteer/Selenium) to search keywords on Google Images.
    *   **Action**: Screenshotting entire Result Pages (SERPs) or image grids. **No individual image downloads.**
*   **Visual Extraction Stack**:
    *   **Color Analysis**:
        *   *Pre-processing*: Remove whitespace/backgrounds.
        *   *Algorithm*: **K-Means Clustering** to find top 5-15 dominant colors.
        *   *Output*: HEX codes sorted by frequency + HSV analysis (for "Neon" vs "Pastel" classification).
    *   **Pattern & Style Recognition**:
        *   *Algorithm*: **CLIP (OpenAI)** or pre-trained Vision Transformers.
        *   *Method*: Zero-shot classification against a predefined style dictionary (e.g., "Vintage Poster", "Pixel Art", "Grunge").
    *   **Composition Detection**:
        *   *Algorithm*: OpenCV (Edge detection, Contour analysis).
        *   *Insights*: Complexity (Minimal vs Busy), Layout (Centered vs All-over).

### 4.3 Module C: The "Design Brain" (Model)
**Goal**: Synthesize inputs into a cohesive creative direction.

*   **7-Dimensional Analysis Model**:
    1.  **Style (25%)**: Core aesthetic (e.g., Cyberpunk).
    2.  **Color (20%)**: Palette & Harmony.
    3.  **Atmosphere (15%)**: Mood/Vibe (e.g., Ethereal, Edgy).
    4.  **Pattern (15%)**: Graphic elements (e.g., Floral, Geometric).
    5.  **Material (10%)**: Texture (e.g., Metallic, Velvet).
    6.  **Composition (10%)**: Visual structure.
    7.  **Tech (5%)**: Rendering style (e.g., 3D Render, Oil Painting).
*   **Compatibility Check**: Logic to ensure Color X and Style Y don't conflict (e.g., Neon colors + Sepia Vintage style = Warning).

### 4.4 Module D: AI Generator & Output
**Goal**: Produce the final asset.

*   **Prompt Construction**:
    *   Templates optimized for specific models (MJ v6, SDXL).
    *   *Structure*: `[Subject/Core Style] + [Visual Descriptors] + [Tech/Camera Specs] + [Negative Constraints]`.
*   **Output Specs**:
    *   Format: DTF-Ready (Direct-to-Film), localized colors, high contrast, transparent bg friendly.

---

## 5. Technical Implementation Details

### 5.1 Technology Stack
| Component | Suggested Tools |
| :--- | :--- |
| **Trend Feed** | `pytrends` (Google), Reddit API, Pinterest `Search Suggest` |
| **Browsing** | Selenium, Playwright (Headless Chrome) |
| **Image Processing** | Python `PIL` (Pillow), `scikit-learn` (K-Means), `OpenCV` |
| **AI Vision** | OpenAI `CLIP`, PyTorch |
| **Backend/Orchestration** | Python (FastAPI), Celery/Redis (Queues) |
| **Frontend** | Next.js / React (for dashboard) |

### 5.2 Daily Automation Schedule (Cron)
*   **00:00** - **Harvest**: Update Seed Keyword Database from APIs.
*   **01:00** - **Hunt**: Batch search & screenshot top 50 trending keywords.
*   **02:00** - **Analyze**: Process screenshots -> Extract JSON Visual Profiles.
*   **03:00** - **Synthesize**: Generate 10-50 curated prompts.
*   **04:00** - **Create**: Batch generation via Image AI.
*   **05:00** - **Publish**: Update internal dashboard / JSON feed.

---

## 6. Example Turn-by-Turn Scenario

**Input**: Keyword *"Y2K"*
1.  **Search**: System searches "Y2K tshirt design" on Google Images.
2.  **Visuals**: Captures screenshots of result grids.
3.  **Analysis**:
    *   *Colors*: Detects Hot Pink (#FF1493) and Cyan (#00FFFF).
    *   *Style tags*: Matches "Chrome", "Butterfly", "Gradient".
    *   *Vibe*: "Playful", "Nostalgic".
4.  **Synthesis**: Confidence Score 85% (High consistency in results).
5.  **Generated Prompt**:
    > "Garment design, Y2K aesthetic, chrome letters and butterfly motif, hot pink and cyan gradient background, high gloss texture, vector art style, centered composition --no distressed --ar 3:4"

---

## 7. Future Expansion
*   **Multimodal Seeds**: Allow image-based seeds (upload a moodboard -> find similar trends).
*   **Product Expansion**: Adapt model for Hoodies, Mugs, or UI Design trends.
*   **Market Feedback Loop**: Integrate sales data to reinforce "winning" patterns.
