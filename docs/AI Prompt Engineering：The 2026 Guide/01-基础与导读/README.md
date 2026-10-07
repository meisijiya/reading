# 一 基础与导读（Chapter 1–3）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

本模块三章奠定全书底座：第一章回答「Prompt Engineering 是什么」（含「How to Use This Book」导读）、第二章讲清楚「与谁对话——LLM 是什么」，第三章给出贯穿全书的「4 C's Framework」。任何模板章节的公式本质都是 4 C's 的细化。

## §1 第1章 What Is Prompt Engineering?

- **章节 UID**: 01
- **章节号**: §1
- **父模块**: 基础与导读
- **原文出处**: [`uid-01-what-is-prompt-engineering.md`](../00-原书档案/fulltext/uid-01-what-is-prompt-engineering.md)

> 📖 **原文**（导读）：This book is designed to take you from prompt beginner to prompt expert — with 320 ready-to-use prompts in the main chapters, 100 bonus prompts in Appendix J, and an expert-techniques appendix built for the 2026 AI landscape.

> 📖 **原文**（§1.1）：In 2026, AI is no longer a novelty. It is infrastructure. It drafts your emails, debugs your code, summarizes your meetings, designs your product mockups, analyzes your spreadsheets, and writes your marketing copy — often before you finish your coffee.

> 📖 **原文**（§1.1）：A prompt is not a question. It is an instruction, a context, a constraint, and a goal — compressed into text that guides the model's reasoning.

> 📖 **原文**（§1.2）：Prompt engineering is the art and science of designing inputs that guide AI models to produce the outputs you actually want. It is not: Guessing magic phrases. Copy-pasting prompts from Twitter without understanding why they work. Hoping the AI will read your mind. One-shot typing and one-shot hoping.

> 📖 **原文**（§1.3）：2022–2023: Early adopters. *2024*: Mainstream use. *2025*: Professional adoption. *2026*: Expert usage. *Build me a multi-step agent that pulls from my CRM, drafts personalized outreach, waits for replies, and escalates to me only the hot leads.*

> 📖 **原文**（§1.4 / 4 C's Preview）：*Clear* — "Write a 500-word blog post about AI marketing strategies for small businesses, targeting entrepreneurs aged 25–40." / *Concise* — "Create 3 LinkedIn posts (150 words each) announcing our new AI marketing tool. Target: marketing managers. Tone: professional but enthusiastic. Include 1 question per post." / *Contextual* — "Write a Python function that processes CSV data from a marketing campaign, calculates ROI, and exports results to a new CSV. Use pandas. Handle missing values." / *Conversational* — "Explain prompt engineering like I'm a marketing professional with 5 years of experience. Use examples from my industry."

> 📖 **原文**（§1.5 五大常见错误）：*The Vague Request / The Overstuffed Prompt / No Examples / Lost Context / One-Shot Thinking*. Fix: 加主题、长度、受众、语气；分步；给示例；按主题开新对话；持续迭代。

> 📖 **原文**（§1 ROI 表）：Novice 1–2 小时/天（基础草稿）→ Intermediate 3–5 小时（内容/代码/分析）→ Expert 6–10+ 小时（完整工作流 / Agents / 自动化流水线）。

> 🧭 **归纳**：第一章给出三件事的「势」——①AI 在 2026 已成基础设施（不是能力，是日常工具），②Prompt Engineering 定义为「设计输入引导模型产生想要输出的艺术+科学」，③所有人与高手的差距就是 Prompt Engineering 能力。**附带产出 4 C's 的预览**（Clear / Concise / Contextual / Conversational），在第三章完整展开。

## §2 第2章 Understanding Large Language Models

- **章节 UID**: 02
- **章节号**: §2
- **父模块**: 基础与导读
- **原文出处**: [`uid-02-understanding-large-language-models.md`](../00-原书档案/fulltext/uid-02-understanding-large-language-models.md)

> 📖 **原文**（§2.1）：LLM stands for Large Language Model — an AI system trained on massive volumes of text (and in 2026, often images, audio, and video) to understand and generate human-like language. The three key components: Neural Networks / Training on Massive Data / Predictive Processing. *An LLM does not "know" things the way a human expert does. It predicts the most likely next token given the prompt and its training.*

> 📖 **原文**（§2.2 2026 主流模型）：*Claude Opus / Sonnet / Haiku*（Anthropic，长上下文+结构化 XML+工具）；*Flagship GPT + Reasoning (o-series) + Efficient*（OpenAI，生态最广+最强推理）；*Gemini Pro/Ultra / Flash*（Google，1M+ token+Workspace 集成）；*Llama*（Meta，开源可自部署）；*Grok*（xAI，实时 X 接入）；*Mistral*（欧盟开源合规替代）。

> 📖 **原文**（§2.3 上下文窗口）：8K tokens ≈ 短章（简单 Q&A）/ 32K–128K ≈ 中篇（文件+持续对话）/ 200K ≈ 整本书（长代码库）/ 1M+ ≈ 小型资料库（整仓+多小时转录+视频）。3 招突破上限：Chunking · Summarize-then-Analyze · Retrieval-Augmented Generation (RAG)。

> 📖 **原文**（§2.4 付费 vs 免费）：Most major providers offer a free tier that's more than enough to learn on. Free tiers typically include a smaller or older model, lower daily limits, and reduced context. That's fine for learning. *Consumer subscriptions (typically around $20/month per provider in 2026) unlock flagship models, longer context, image generation, file uploads, and higher limits.*

> 📖 **原文**（§2.5 采样温度）：0.0 确定性/代码与事实答案 → 0.3–0.5 平衡/分析写作 → 0.7–0.9 创意/头脑风暴 → 1.0+ 实验性。Top-P 同方向；API 与 playground 中可手动调，普通聊天 App 中则由系统决定。

> 📖 **原文**（§2.6 限制与陷阱）：*Hallucinations*（模型自信编造——给「不知道」权限、要源、用 RAG、用 reasoning model）；*Bias*（明确请求多元视角+让模型自审）；*Knowledge Cutoffs*（用联网模型或自带最新上下文的 RAG）；*Cost Awareness*（长 prompt 贵、reasoning tokens 贵、缓存省、廉价模型做简单任务）。

> 🧭 **归纳**：第二章是「与谁对话」的技术参数表。**记 4 件事实**就能与任何 LLM 高效协作：①LLM = 神经网络 + 大数据 + 预测下一个 token；②主流 6 家选谁看「最长上下文 / 推理 / 开源 / 实时」四维；③上下文窗口 ≠ 用得好，大内容要 chunk + summarize + RAG；④限制（幻觉/偏见/截止/成本）都能用具体提示策略缓解，无需当成无法跨越的硬约束。

## §3 第3章 The 4 C's Framework

- **章节 UID**: 03
- **章节号**: §3
- **父模块**: 基础与导读
- **原文出处**: [`uid-03-the-4-c-s-framework.md`](../00-原书档案/fulltext/uid-03-the-4-c-s-framework.md)

> 📖 **原文**（§3 完整提示公式）：*[Role] + [Situation] + [Task] + [Constraints] + [Format] + [Tone]*. 例：Role: Senior marketing director with 15 years of experience / Situation: Launching a new SaaS product with a $500 budget / Task: Create a 30-day marketing plan / Constraints: No paid ads, focus on organic growth / Format: Week-by-week action plan with specific tasks / Tone: Practical and actionable — this should read like a peer handing me a playbook, not a textbook.

> 📖 **原文**（§3.1 Clear 模板）：*[Task Type]: [Specific task] / [Output Format]: [Length / structure] / [Audience]: [Who will use this] / [Constraints]: [Limitations] / [Example]: [Optional — what good looks like]*. 反例: "Write about marketing." → 正例: "Create a marketing strategy outline / Write a marketing email / Analyze marketing campaign performance"。

> 📖 **原文**（§3.2 Concise 公式）：*[Action] + [Subject] + [Constraints] + [Format]*. "Write 3 LinkedIn posts about AI marketing, 150 words each, professional tone, include 1 question"（vs 44 词寒暄版）。三招改造长 prompt：删 filler / 合相关子句 / 用直接命令不用 please。

> 📖 **原文**（§3.3 上下文三角）：Role: 你是谁 / Situation: 现在在什么场景下 / Goal: 你想要什么 + Constraints + Output。完整 Contextual 模板：*Role + Situation + Goal + Constraints + Output*。

> 📖 **原文**（§3.4 Conversational 同理测试）：每次发 prompt 前问自己：①我会这样跟同事说话吗？②这像自然对话吗？③我具体而不机械吗？机器人腔："The user requests marketing content." → 对话腔："I need help creating marketing content."

> 📖 **原文**（§3 常用 prompt 结构 4 种）：*The Problem-Solver*（"I'm facing X. Here's what I've tried. What would you do differently?"）/ *The Creator*（"Create Y about X. Style: Y. Audience: Z."）/ *The Analyzer*（"I have Y. What insights? What should I do next?"）/ *The Improver*（"Here's what I have: Y. Make it Z."）。

> 📖 **原文**（§3 迭代法）：One prompt rarely nails it. Use conversation to refine: 1) First prompt — get the bones right. 2) Second prompt — refine the details. 3) Third prompt — polish and optimize.

> 🧭 **归纳**：4 C's 是本书核心框架。**C1 Clear** = 「任务类型 + 输出格式 + 受众 + 约束 + 可选示例」五要素，告别「写点营销」式空 prompt；**C2 Concise** = 短直不冗余，但 concise ≠ terse（真正需要的 context 不删）；**C3 Contextual** = Role / Situation / Goal / Constraints / Output 五件套，提供诊断式背景；**C4 Conversational** = 用「你/我」对话语言，过「Empathy Test」自检。完整公式 = Role + Situation + Task + Constraints + Format + Tone。所有 Ch 4-10 的场景公式都是这 4 C's 的特化展开。**三步迭代**贯穿全书（初稿→打磨→润色）。
