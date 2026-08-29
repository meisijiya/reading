# 二 场景 Prompt 模板库（Chapter 4–8）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

本模块五章 = 270 条跨场景模板。每章一套专属公式 + 多分类。**所有公式本质都是第 3 章「4 C's Framework」的特化**——写入 prompt 时仍要先满足 Clear+Concise+Contextual+Conversational，再套本场景的 5 要素。

## §4 第4章 Chat & Conversation Prompts

- **章节 UID**: 04
- **章节号**: §4
- **父模块**: 场景 Prompt 模板库
- **原文出处**: [`uid-04-chat-conversation-prompts.md`](../00-原书档案/fulltext/uid-04-chat-conversation-prompts.md)

> 📖 **原文**（§4 Chat Prompt Framework）：*[Opening] + [Context] + [Request] + [Follow-up]*. 例：Opening: "Hi, I'm working on my marketing strategy." / Context: "For a SaaS product with 10 employees." / Request: "What are 5 effective marketing strategies?" / Follow-up: "Can you elaborate on the most cost-effective one?"

> 📖 **原文**（§4 五类 50 条）：*Opening Prompts (1–10)*：通用开场、问题陈述、学习开场、脑暴开场、分析开场、对比开场、策略开场、批评开场、叙事开场、角色开场。*Context-Building (11–20)*：背景上下文、假设检查、Gap 分析、视角请求、约束明确、优先级评估、成功定义、风险识别、替代场景、反馈请求。*Request (21–30)*：澄清请求、举例、对比、步骤分解、时间线、预算受限、资源请求、模板请求、清单请求、推荐请求。*Follow-Up (31–40)*：细化举例、对比追问、批评请求、改进请求、简化请求、深挖请求、实操请求、边界请求、整合请求。*Refinement (41–50)*：语气调整、长度调整、格式变更、受众调整、风格变更、详细度、去 jargon、加例、结构改造、行动项抽取。

> 📖 **原文**（§4 Socratic 五问）：*"What makes you think that? / Can you elaborate on that point? / How does that connect to what you said earlier? / What are the assumptions behind that? / Can you give me an example?"*

> 🧭 **归纳**：50 条 Chat 模板按对话生命周期组织——**打开话题 → 搭上下文 → 提请求 → 追问深挖 → 润色定型**。使用时不要单条发，先发"打开"再自然过渡到"请求"，按对方回答质量决定是否进入"追问"。**Socratic 五问**与**5 轮迭代法**（广→窄→深→具→行动）是 Chat 场景的两个加速器。

## §5 第5章 Writing & Content Creation Prompts

- **章节 UID**: 05
- **章节号**: §5
- **父模块**: 场景 Prompt 模板库
- **原文出处**: [`uid-05-writing-content-creation-prompts.md`](../00-原书档案/fulltext/uid-05-writing-content-creation-prompts.md)

> 📖 **原文**（§5 五要素写作公式）：*[Task] + [Topic/Subject] + [Format/Length] + [Audience] + [Tone/Style]*. 反例（缺 4 要素）："Write a blog post about marketing." → 正例（5 要素齐）："Write a 700-word blog post about AI marketing strategies for small business owners, using a professional but approachable tone with real-world examples."

> 📖 **原文**（§5 65 条六类）：*Blog & Article (51–65, 15 条)*：标准、Listicle、How-To、对比文、案例研究、Thought Leadership、PAS、Storytelling、FAQ、Newsjacking、Guest Post Pitch、SEO、Evergreen、Contrarian、Recap。*Social Media (66–80, 15 条)*：LinkedIn、Twitter/X、IG、TikTok/Reels、Newsletter、Carousel、Quote、Poll、Story Starter、AMA、Case Study Snippet、Tip、BTS、Milestone、Question-Driven。*Professional (81–95, 15 条)*：3-Email Sequence、Cold Outreach、Follow-Up、Newsletter、Executive Summary、Pitch Deck、Case Study Summary、Meeting Agenda、Report Summary、Project Proposal、Progress Update、Post-Mortem、Cover Letter、Networking、Referral Request。*Creative (96–105, 10 条)*：Short Story、Brand Story、Testimonial、Script Outline、Series Opener、Product Description、Landing Page、Subject Line、Ad Copy、Elevator Pitch。*Resume & Career (106–110, 5 条)*：Resume Bullet、LinkedIn Summary、Interview Answer STAR、Cover Letter Paragraph、Promotion Request。*Editing & Refinement (111–115, 5 条)*：Tone Adjuster、Jargon Remover、Conciseness Improver、Flow Improver、Grammar & Style Pass。

> 🧭 **归纳**：65 条覆盖 6 大场景，**统一公式 = Task + Topic + Format/Length + Audience + Tone/Style**。最常见的失败是「缺 Format（"5,000 字也合规？"）+ 缺 Audience（"对谁写"）+ 缺 Tone（"口气"）」三件事。**对生成结果不满意时，永远先用 P111-115 润色 prompt 套娃**：调语气/去 jargon/砍字数/顺逻辑——比重新写一遍稳。

## §6 第6章 Analysis & Research Prompts

- **章节 UID**: 06
- **章节号**: §6
- **父模块**: 场景 Prompt 模板库
- **原文出处**: [`uid-06-analysis-research-prompts.md`](../00-原书档案/fulltext/uid-06-analysis-research-prompts.md)

> 📖 **原文**（§6 Analysis Framework）：*[Data/Context] + [Analysis Type] + [Specific Focus] + [Output Format]*. 例：Data: "Here's my marketing campaign data for Q1..." / Analysis Type: "Analyze the performance." / Focus: "Identify what worked and what didn't." / Output Format: "3 key insights with actionable recommendations."

> 📖 **原文**（§6 50 条七类）：*Data Analysis (116–125, 10)*：基本摘要、趋势、对比、相关性、异常值、性能指标、Segment、5-Whys、SWOT、Gap。*Market Research (126–135, 10)*：TAM/SAM/SOM、Competitor Deep Dive、ICP、Pricing、Market Entry、Product-Market Fit、Industry Trends、Product SWOT、GTM、Customer Journey Map。*Business Analysis (136–145, 10)*：财务、运营效率、ROI、Business Model、增长策略、风险评估、KPI Dashboard、预算、战略规划、退出策略。*Academic (146–150, 5)*：文献综述、研究问题、方法设计、数据解读、学术摘要。*Sentiment (151–155, 5)*：Review 分析、品牌感知、Feedback 摘要、Survey 分析、Crisis Response。*Competitive Intel (156–160, 5)*：网站分析、Product Comparison Matrix、营销分析、Pricing 反推、市场定位。*Trend Identification (161–165, 5)*：趋势识别、Pattern Recognition、Innovation、Disruption、未来 3 年预测。

> 🧭 **归纳**：分析 prompt 与写作 prompt 的关键差别是——**先喂数据/上下文，再要动作建议**。「写一篇市场分析」是 P137 容易翻车的写法；「把这组 Q1 数据跑一下，给我 3 条 actionable insights」才是 P121/152 想要的。50 条按「自有数据 → 行业数据 → 学术方法」递进；**SWOT / 5-Whys / Gap** 这三个 Pattern 是各场景的复用主力（自带表格结构最稳）。

## §7 第7章 Coding & Technical Prompts

- **章节 UID**: 07
- **章节号**: §7
- **父模块**: 场景 Prompt 模板库
- **原文出处**: [`uid-07-coding-technical-prompts.md`](../00-原书档案/fulltext/uid-07-coding-technical-prompts.md)

> 📖 **原文**（§7 四要素技术公式）：*[Task] + [Language/Tool] + [Constraints] + [Context/Requirements]*. 反例："Write code for a database connection." → 正例："Write a Python function using psycopg2 to connect to a PostgreSQL database. Include error handling, connection pooling, and a connection string from environment variables."

> 📖 **原文**（§7 45 条六类）：*Code Generation (166–180, 15)*：Function、Class、Algorithm、API Endpoint、SQL、Config、Script、Data Structure、Dockerfile、CI/CD (GitHub Actions)、Regex、Unit Test、DB Migration、API Client、CLI。*Code Explanation (181–190, 10)*：逐行解释、架构、性能、Security Review (P184 OWASP Top 10)、Best Practices、Legacy、Debug、依赖、PR Review、Tech Debt。*Python (191–195, 5)*：Pandas、FastAPI、Pydantic、asyncio、Dataclass、Context Manager。*JS/TS (196–200, 5)*：React TS 组件、Node Express + Zod、Utility Type、Async + AbortController、ESLint flat config。*SQL & DB (201–205, 5)*：复杂查询、Index、Transaction、Migration、View。*DevOps (206–210, 5)*：Terraform、Kubernetes Manifest、AWS Lambda、CloudWatch 告警、Security Group。

> 🧭 **归纳**：**技术 prompt 的 4 大硬要求**：①**语言+版本号**（Python 3.12，不是 Python；React 19，不是 React）；②**错误处理需求**（必须显式 "with proper error handling / typed errors"）；③**现有代码库上下文**（"for the existing FastAPI app in /api/v1/"）；④**测试 + 文档要求**（不要再逐条问 "please write tests"）。**P184 Security Review** 引用 OWASP Top 10，是少数"prompt 本身有公信力背书"的模板——生产前必跑。

## §8 第8章 Image Generation Prompts

- **章节 UID**: 08
- **章节号**: §8
- **父模块**: 场景 Prompt 模板库
- **原文出处**: [`uid-08-image-generation-prompts.md`](../00-原书档案/fulltext/uid-08-image-generation-prompts.md)

> 📖 **原文**（§8 五要素图像公式）：*[Subject] + [Style/Art Medium] + [Composition] + [Lighting] + [Technical Details]*. 反例："Generate a logo for a tech company." → 正例："Modern tech company logo with an abstract geometric shape, minimalist design, blue and white color scheme, flat vector style, clean lines, high resolution."

> 📖 **原文**（§8 2026 平台对照）：*Midjourney* 强艺术美学 · *DALL-E / GPT Image* 强商业安全+文字入图 · *Stable Diffusion (+ Flux)* 开源可控 ControlNet / LoRA / 本地部署 · *Google Imagen* 极致摄影 · *Ideogram* 强排版字体 · *Runway / Sora / Veo* 文生视频+图生视频。

> 📖 **原文**（§8 60 条六类）：*General (211–220, 10)*：产品 Mock、概念艺术、社媒图、信息图、插图、摄影场景、抽象、角色、UI/UX、品牌识别。*Midjourney-Style (221–230, 10)*：Artist Masterpiece、Anime、Cyberpunk、Oil Painting、Watercolor、Vector、3D Render (UE5)、Retro 1980s、Minimalist、Surreal。*DALL-E/GPT Image (231–240, 10)*：商业产品、文字入图、Stock Photo、儿童绘本、食谱摄影、人物肖像、建筑渲染、时装设计、医疗插画、教学图。*Stable Diffusion / Flux (241–250, 10)*：ControlNet、Inpainting、Upscaling、LoRA、Pose、Depth、Canny、Segmentation、Tile、Detail Inpainting。*Style-Specific (251–260, 10)*：Pixar、Studio Ghibli、Wes Anderson、Van Gogh、Blade Runner、Synthwave、Minimalist、Watercolor、Line Art、Pixel Art。*Lighting & Atmosphere (261–270, 10)*：Golden Hour、Neon、Studio、Cinematic、Natural、Backlight、Low-Key、High-Key、Ambient、Spot。

> 🧭 **归纳**：图像 prompt 是「艺术 > 科学」。公式层面的 **5 要素**是底线（很多新手只写 Subject 一项，所以图很拉），但要稳定出图必须叠加 2 个 2026 关键技巧：①**"in the style of [具体艺术家/工作室/作品]" + 技术参数**（如 "8K, cinematic lighting, trending on ArtStation"）；②**Commercial/Commercial Use 显式声明**避免商用侵权。**Midjourney / DALL-E / SD 三家提示词写法差异极大**——参考 P221-230 (Midjourney 强调美学标签) vs P231-240 (DALL-E 强调商业语) vs P241-250 (SD 强调 ControlNet 控制项)。
