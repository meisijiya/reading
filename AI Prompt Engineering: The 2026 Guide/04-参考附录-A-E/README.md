# 四 参考附录 A–E（Appendix A–E）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

本模块五章是参考卷——目录、模型对照、工具、学习资源、检查清单。需要时按主题打开查阅，不参与主线流程。

## §A Appendix A: The 320-Prompt Catalog

- **章节 UID**: 12
- **附录号**: A
- **父模块**: 参考附录 A–E
- **原文出处**: [`uid-12-the-320-prompt-catalog.md`](../00-原书档案/fulltext/uid-12-the-320-prompt-catalog.md)

> 📖 **原文**（Catalog 总表）：Chat & Conversation (50) — Chapter 4：Prompts 1–10 Opening / 11–20 Context-Building / 21–30 Request / 31–40 Follow-Up / 41–50 Refinement。Writing & Content Creation (65) — Chapter 5：51–65 Blog (15) / 66–80 Social (15) / 81–95 Professional (15) / 96–105 Creative (10) / 106–110 Resume (5) / 111–115 Editing (5)。Analysis & Research (50) — Chapter 6：116–125 Data (10) / 126–135 Market (10) / 136–145 Business (10) / 146–150 Academic (5) / 151–155 Sentiment (5) / 156–160 Competitive (5) / 161–165 Trend (5)。Coding & Technical (45) — Chapter 7：166–180 Code Gen (15) / 181–190 Explain (10) / 191–195 Python (5) / 196–200 JS/TS (5) / 201–205 SQL (5) / 206–210 DevOps (5)。Image Generation (60) — Chapter 8：211–220 General (10) / 221–230 Midjourney (10) / 231–240 DALL-E (10) / 241–250 SD/Flux (10) / 251–260 Style (10) / 261–270 Lighting (10)。Business Applications (50) — Chapter 10：271–280 Daily (10) / 281–290 Marketing/Sales (10) / 291–300 Ops (10) / 301–310 Entrepreneur (10) / 311–320 Automation (10)。Bonus (100) — Appendix J：B1–B20 Everyday / B21–B40 Business / B41–B60 Creative / B61–B75 Technical / B76–B90 Analysis / B91–B100 Advanced。

> 🧭 **归纳**：**420 Prompts 完整索引**（主册 320 + Bonus 100）。**编号法则**：主册 1–320 与章节号无关，仅按所在章节出现顺序；加餐 B1–B100 与章节号无关，仅按 Appendix J 内部分组顺序。**找 prompt 的最快路径**：先用速查表定位场景/类别，再按编号回读 `00-原书档案/fulltext/uid-04..uid-08, uid-10, uid-21`。

## §B Appendix B: Model Landscape 2026

- **章节 UID**: 13
- **附录号**: B
- **父模块**: 参考附录 A–E
- **原文出处**: [`uid-13-model-landscape-2026.md`](../00-原书档案/fulltext/uid-13-model-landscape-2026.md)

> 📖 **原文**（前言）：*AI model names, pricing, and capabilities change quickly. Treat this as a snapshot; verify current details on each provider's website before committing to one.*

> 📖 **原文**（Frontier Text & Multimodal 表）：*Anthropic Claude Opus / Sonnet / Haiku*（200K+ tokens，最强推理 / 性价比日驾 / 高吞吐低成本 RAG）*OpenAI Flagship GPT / Reasoning (o-*) / Efficient*（128K+，生态最广 / 思考 tokens 额外收费 / 性价比快模型）*Google Gemini Pro/Ultra / Flash*（1M–2M tokens，Workspace 集成 / 极速高吞吐）*Meta Llama*（128K+，开源可自部署）*xAI Grok*（128K+，实时 X）*Mistral Large/Mixtral*（128K+，欧盟合规）。

> 📖 **原文**（图像表）：*Midjourney* 极致美学艺术 / *DALL-E / GPT Image* 商业安全+文字入图 / *Google Imagen* 极致摄影 / *Stable Diffusion* 开源+ControlNet+LoRA+本地 / *Flux* 最强开源图像 / *Ideogram* 强排版字体。

> 📖 **原文**（视频表）：*Sora* 电影级文生视频 · *Veo* 长时高高保真 · *Runway* 编辑友好支持图生视频 · *Pika / Kling* 快迭代低成本。

> 📖 **原文**（价格趋势）：Most flagship consumer plans cluster around $20/month, with premium/pro tiers around $100–$200/month for heaviest users. API pricing is billed per million input and output tokens, with flagship models typically more expensive than mid-tier models by 3–5x. Prompt caching and batch APIs can dramatically reduce cost on repeated or non-urgent workloads.

> 🧭 **归纳**：**2026 模型版图**：①**文字首选**看你需求——默认 Sonnet/GPT-Flagship/Flash/智驾三选一；②**超长文档** Gemini Pro；③**强推理** Opus 或 o-series；④**开源私有** Llama/Mistral via Ollama vLLM；⑤**图首选** Midjourney（艺术）/ DALL-E（商业+文字）/ Imagen（摄影）/ SD/Flux（可控+本地）；⑥**视频** Sora/Veo/Runway 三家分占电影/长时/编辑。**价格锚点：$20/mo、$100-200/mo 重度；API 按 token 计费，旗舰比中端贵 3-5 倍**。作者特别强调"快照式"——价格和型号随时变动，决策前必看 providers 官网。

## §C Appendix C: Prompt Engineering Tools

- **章节 UID**: 14
- **附录号**: C
- **父模块**: 参考附录 A–E
- **原文出处**: [`uid-14-prompt-engineering-tools.md`](../00-原书档案/fulltext/uid-14-prompt-engineering-tools.md)

> 📖 **原文**（七大类目）：*Chat Interfaces*：ChatGPT（自定义 GPT+图像+Projects）/ Claude.ai（Artifacts+Projects+MCP 连接器）/ Gemini（Gems+Workspace）/ Grok / Perplexity（重视引用源）/ Poe（多模型聚合）。*Developer Frameworks*：LangChain / LlamaIndex / DSPy（编程而非 prompt）/ 各家官方 SDK / Vercel AI SDK / Instructor（Pydantic 结构化）。*Evaluation & Observability*：LangSmith / Braintrust / Helicone / PromptFoo。*RAG and Vector Stores*：Pinecone / Weaviate / Qdrant / Chroma / Milvus / pgvector / LanceDB。*Automation Platforms*：Zapier / Make / n8n / Pipedream。*Prompt Libraries*：PromptHero / PromptBase / LearnPrompting.org / Anthropic Prompt Library / OpenAI Cookbook。*Local and Open-Source*：Ollama / llama.cpp / LM Studio / vLLM。

> 🧭 **归纳**：工具栈按"**聊 → 写代码 → 测评估 → 接知识库 → 自动触发 → 抄模板 → 本地部署**"七层堆叠。**2026 关键趋势**：①MCP 连接器（Claude/GPT/Gemini 都在推）让模型直接连 Gmail/GitHub/Slack/Notion/Postgres；②DSPy 等"编程式 prompt"开始取代手写 prompt（CSP-by-example）；③**Eval/观测平台**（LangSmith/Braintrust/Helicone）成为严肃 prompt 工程标配——大附录 G 第 7 节还会展开。

## §D Appendix D: Learning Resources

- **章节 UID**: 15
- **附录号**: D
- **父模块**: 参考附录 A–E
- **原文出处**: [`uid-15-learning-resources.md`](../00-原书档案/fulltext/uid-15-learning-resources.md)

> 📖 **原文**（五类资源）：*Free Courses*：Learn Prompting (learnprompting.org) / Anthropic Prompt Engineering Tutorial / OpenAI Cookbook / DeepLearning.AI short courses (含 ChatGPT PE + LangChain) / Google Prompt Engineering Guide。*Paid Courses*：DeepLearning.AI "Prompt Engineering for Developers" / Coursera "AI for Everyone" (Andrew Ng) / Maven 等付费项目。*Communities*：r/PromptEngineering / r/LocalLLaMA / Prompt Engineering Discord / LinkedIn（关注各 provider 与独立 prompt engineer）。*Research*：arXiv cs.CL / The Gradient / Import AI / Latent Space 周更邮件 / Lex Fridman / Dwarkesh / Latent Space Podcast。*Official Model Docs (Bookmark)*：docs.anthropic.com · platform.openai.com/docs · ai.google.dev · docs.mistral.ai · llama.com。

> 🧭 **归纳**：**学习路径最小集**：①**先通读本书 1-3 章**打底；②**免费课程用 DeepLearning.AI 系列**（含 LangChain）搭工程能力；③**研究阶段读 arXiv cs.CL + 三个 Newsletter**保持前沿；④**官方文档必须常驻收藏夹**——任何严肃 prompt 工程都得问"这个模型最新版本支持什么"。

## §E Appendix E: Prompt Engineering Checklists

- **章节 UID**: 16
- **附录号**: E
- **父模块**: 参考附录 A–E
- **原文出处**: [`uid-16-prompt-engineering-checklists.md`](../00-原书档案/fulltext/uid-16-prompt-engineering-checklists.md)

> 📖 **原文**（Pre-Prompt Checklist 8 项）：*☐ Goal / ☐ Audience / ☐ Format (length / structure / headings / file type) / ☐ Tone (formal / casual / technical / playful) / ☐ Context (does model need background?) / ☐ Examples (1–2 examples help?) / ☐ Constraints (length / cost / model / framework) / ☐ Output (plain / Markdown / JSON / code)*.

> 📖 **原文**（Post-Prompt Checklist 6 项）：*☐ Does it meet the goal? / ☐ Is it clear and complete? / ☐ Are there factual errors? / ☐ Are there hallucinated sources? / ☐ Can I improve this with one refinement prompt? / ☐ Should I save this prompt for reuse?*

> 📖 **原文**（Prompt Library Checklist 5 项）：*☐ Give it a short, memorable name. / ☐ Document what placeholders ([brackets]) it expects. / ☐ Note the model(s) it works well on. / ☐ Include one example of desired output. / ☐ Record any known failure modes or edge cases.*

> 📖 **原文**（Safety & Quality Checklist 6 项）：*☐ I've verified key facts against primary sources. / ☐ There are no hallucinated quotes, statistics, or citations. / ☐ The tone matches the brand. / ☐ Tests pass (if code). / ☐ No private data was leaked into the output. / ☐ I own the rights to the generated content for my use case.*

> 🧭 **归纳**：**4 个清单 = 4 个时间点**：发之前（Pre）/ 收到后立刻（Post）/ 入库时（Library）/ 发出去前（Safety）。**Pre 清单本质就是 4 C's + 输出形式**的填空版；**Post 清单的核心问题是"要不要保存"**——这是把一次 prompt 变成团队资产的唯一路径。**Safety 清单的 6 项都是发布前死门**，特别是「核对事实」「无引用幻觉」「无隐私泄漏」「拥有版权」——公司对外内容必跑。
