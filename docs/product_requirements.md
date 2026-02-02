# 产品需求文档：自动化 T 恤设计生成器

## 1. 产品概述
**"AI 员工" 设计生成器** 是一个端到端的自动化系统，旨在简化 T 恤生产流程。它扮演一个自主设计师的角色，负责研究市场趋势、构思独特设计、生成高保真样机，并准备在 Etsy 等平台上销售。

## 2. 用户旅程与核心流程

### 第一阶段：市场调研 (输入) - **[需配置化]**
*   **目标**：识别当前和新兴的时尚趋势，确保设计的相关性。
*   **机制**：
    *   **配置化来源**：系统需支持通过配置文件 (`sources.json`) 或管理后台定义抓取源：
        *   **类型 A (社媒)**：Pinterest, Instagram (特定 Hashtag 如 #streetwear2025)。
        *   **类型 B (新闻)**：Hypebeast, Vogue Business, WGSN 摘要。
        *   **类型 C (搜索)**：Google Images 关键词监控。
    *   **数据点**：捕捉视觉趋势、关键词和流行美学风格（例如 "Oversized Streetwear", "Y2K Glam"）。

### 第二阶段：AI 分析与创意生成 (处理) - **[核心逻辑]**
*   **目标**：将原始趋势转化为结构化、可执行的设计概念。
*   **功能**：**"设计灵感" (Design Ideas) 模块**
    *   **深度分析**：AI 将趋势分解为具体属性（JSON 结构）：
        *   **Theme**: 核心概念 (e.g., "Cyberpunk Utility")
        *   **Style**: 剪裁/版型 (e.g., "Boxy fit", "Drop-shoulder")
        *   **Colors**: 详细色卡 (e.g., "Matte black base with neon amber highlights")
        *   **Elements**: 图案/材质 (e.g., "Kanji typography", "Geometric back prints")
        *   **Mood**: 氛围 (e.g., "Edgy", "Retro-nostalgic")
    *   **提示词升级 (Prompt Engineering) 逻辑**：
        *   **转化公式**：`[摄影风格/媒介] of a [Style] t-shirt featuring [Theme] graphics, [Elements] details, [Colors] scheme, [Mood] lighting --v [ModelVersion]`
        *   **示例**：*Professional product photography of a Boxy fit t-shirt featuring Cyberpunk Utility graphics, Kanji typography and geometric back prints, Matte black base with neon amber highlights, Edgy dramatic lighting, 8k resolution, photorealistic.*
    *   **用户交互**：用户可以查看这些细节及生成的 Prompt，支持手动修改或"重抽样"。

### 第三阶段：图像生成 (输出)
*   **目标**：创建即可投产的视觉资产。
*   **功能**：**"画廊" (Gallery)**
    *   **批量生成**：系统将验证后的创意输入图像生成模型。
    *   **输出**：生成一批（例如 10 张）高分辨率的 T 恤样机图。
    *   **可视化**：设计直接展示在逼真的模特或服装模型上。

### 第四阶段：分发 (集成)
*   **目标**：通过上架销售来实现设计变现。
*   **当前状态**：
    *   **邮件导出**：用户目前可以将生成的 10 个设计通过邮件发送给自己。
    *   **必要需求**：
    *   **Etsy 集成**：最终系统必须能够自动将选定的设计上传到 Etsy（以及潜在的其他平台）作为按需打印 (POD) 商品，完成 "被动收入" 闭环。

### 第五阶段：视频营销 (新需求)
*   **目标**：利用生成式视频 AI 制作适合 TikTok/Reels 的短视频。
*   **工具链**：
    *   **Nanobanana / Sora 2**：
        *   **输入**：从第三阶段生成的 T 恤样机图（静态图片）。
        *   **动作指令**：自动生成动作 Prompt（如 "Slow motion zoom, model walking in neon city, fabric flowing"）。
        *   **输出**：5-10 秒的高清动态视频。
    *   **应用场景**：作为 Etsy 商品的主图视频，或自动发布到 TikTok 营销账号。

## 3. 关键功能需求

| 功能领域 | 需求描述 |
| :--- | :--- |
| **趋势抓取器** | 一个强大的爬虫，用于从视觉搜索引擎获取实时趋势数据。 |
| **LLM 分析 Agent** | 一个具备视觉理解（如果输入是图片）或文本综合能力的 AI Agent，能将趋势分解为结构化的 JSON 属性（主题、风格、颜色等）。 |
| **提示词升级器** | 将结构化属性转化为高性能图像生成提示词的逻辑（例如添加技术关键词如 "4k", "studio lighting", "vector style"）。 |
| **图像生成 API** | 集成高质量图像生成器（如 Midjourney API, DALL-E 3, 或 Stable Diffusion）。 |
| **电商 API** | 集成 Etsy API，以便直接从生成的资产创建草稿或发布商品列表。 |

## 4. UI/UX 观察
*   **透明度**："灵感" (Ideas) 菜单对于建立用户信任至关重要，它展示了 AI 是 *如何* 得出设计概念的。
*   **简洁性**：流程是线性的（灵感 -> 创意 -> 画廊），最大限度地减少了用户摩擦。
*   **美学**：界面应反映工具的创意属性——干净、现代且视觉优先。
