# 三 Prompt 与上下文（§5-§6）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

## §5 第5章 Prompt Engineering

- **章节 UID**: 06
- **章节号**: §5
- **字数**: 12,527
- **父模块**: Prompt 与上下文
- **原文出处**: [`uid-06-Prompt-Engineering.md`](../00-原书档案/fulltext/uid-06-Prompt-Engineering.md)

> 📖 **原文**（§5.0）：Prompt engineering refers to the process of crafting an instruction that gets a model to generate the desired outcome. Prompt engineering is the easiest and most common model adaptation technique. Unlike finetuning, prompt engineering guides a model's behavior without changing the model's weights.

> 📖 **原文**（§5.0）：*The problem is not with prompt engineering. It's a real and useful skill to have. The problem is when prompt engineering is the only thing people know.* To build production-ready AI applications, you need more than just prompt engineering.

> 📖 **原文**（§5.1 Prompt 构成）：A prompt generally consists of one or more of the following parts: (1) Task description; (2) Example(s) of how to do this task; (3) The task.

> 📖 **原文**（§5.1）：For prompting to work, the model has to be able to follow instructions. If a model is bad at it, it doesn't matter how good your prompt is, the model won't be able to follow it. … How much prompt engineering is needed depends on how robust the model is to prompt perturbation.

> 📖 **原文**（§5.2 In-context learning）：Teaching models what to do via prompts is also known as *in-context learning*. … Each example provided in the prompt is called a *shot*. Teaching a model to learn from examples in the prompt is also called *few-shot learning*. … When no example is provided, it's *zero-shot learning*.

> 📖 **原文**（§5.2）：For GPT-3, few-shot learning showed significant improvement compared to zero-shot learning. However, for the use cases in Microsoft's 2023 analysis, few-shot learning led to only limited improvement compared to zero-shot learning on GPT-4 and a few other models. This result suggests that as models become more powerful, they become better at understanding and following instructions, which leads to better performance with fewer examples.

> 📖 **原文**（§5.3 System vs User Prompt）：Many model APIs give you the option to split a prompt into a *system prompt* and a *user prompt*. You can think of the system prompt as the task description and the user prompt as the task.

> 📖 **原文**（§5.3）：Under the hood, *the system prompt and the user prompt are concatenated into a single final prompt before being fed into the model*. … The system prompt comes first in the final prompt, and the model might just be better at processing instructions that come first. … The model might have been post-trained to pay more attention to the system prompt, as shared in the OpenAI paper "The Instruction Hierarchy".

> 📖 **原文**（§5.3 Chat Template）：Different models use different chat templates. The same model provider can change the template between model versions. For example, for the Llama 3 chat model, Meta changed the template to the following: `system\n{{ system_prompt }}user\n{{ user_message }}assistant\n` … Accidentally using the wrong template can lead to bewildering performance issues.

> 📖 **原文**（§5.3 Context Length）：Within five years, context length grew 2,000 times from GPT-2's 1K context length to Gemini-1.5 Pro's 2M context length. A 100K context length can fit a moderate-sized book. A 2M context length can fit approximately 2,000 Wikipedia pages and a reasonably complex codebase such as PyTorch.

> 📖 **原文**（§5.3 Needle in a Haystack）：Research has shown that a model is much better at understanding instructions given at the beginning and the end of a prompt than in the middle. … All the models tested seemed much better at finding the information when it's closer to the beginning and the end of the prompt than the middle.

> 📖 **原文**（§5.4 最佳实践）：Write Clear and Explicit Instructions · Provide Sufficient Context · Break Complex Tasks into Simpler Subtasks · Give the Model Time to Think · Iterate on Your Prompts · Evaluate Prompt Engineering Tools · Organize and Version Prompts.

> 📖 **原文**（§5.4 Clear Instructions）：If you want the model to score an essay, explain the score system you want to use. Is it from 1 to 5 or 1 to 10? If there's an essay the model's uncertain about, do you want it to pick a score to the best of its ability or to output "I don't know"?

> 📖 **原文**（§5.4 Decomposition）：Prompt decomposition not only enhances performance but also offers several additional benefits: Monitoring · Debugging · Parallelization · Effort. … One downside of prompt decomposition is that it can increase the latency perceived by users, especially for tasks where users don't see the intermediate outputs.

> 📖 **原文**（§5.4 CoT）：CoT means explicitly asking the model to think step by step, nudging it toward a more systematic approach to problem solving. … The simplest way to do CoT is to add "think step by step" or "explain your decision" in your prompt. … Self-critique means asking the model to check its own outputs.

> 📖 **原文**（§5.4 Iterate & Version）：As you experiment with different prompts, make sure to test changes systematically. *Version your prompts.* Use an experiment tracking tool. Standardize evaluation metrics and evaluation data so that you can compare the performance of different prompts.

> 📖 **原文**（§5.5 Tools）：Tools that aim to automate the whole prompt engineering workflow include OpenPrompt and DSPy. … Many tools aim to assist parts of prompt engineering. For example, Guidance, Outlines, and Instructor guide models toward structured outputs.

> 📖 **原文**（§5.5 Tools 警告）：First, prompt engineering tools often generate hidden model API calls, which can quickly max out your API bills if left unchecked. … *You might want to start by writing your own prompts without any tool*. This will give you a better understanding of the underlying model and your requirements.

> 📖 **原文**（§5.6 Defensive）：There are three main types of prompt attacks that, as application developers, you want to defend against: (1) Prompt extraction; (2) Jailbreaking and prompt injection; (3) Information extraction.

> 📖 **原文**（§5.6 风险）：Prompt attacks pose multiple risks for applications: Remote code or tool execution · Data leaks · Social harms · Misinformation · Service interruption and subversion · Brand risk.

> 🧭 **归纳**：Prompt 工程是"最便宜、最先用"的优化手段，但它不等于"灵机一动改几个词"——它是工程学科。**Prompt 三段式结构**：任务描述 + 示例 + 任务本身；可拆 system prompt（任务描述）/ user prompt（任务）。**为什么它能 work**（in-context learning）：模型从 prompt 中的示例学到新行为，不动权重；GPT-3 时代 few-shot 显著好于 zero-shot，但 GPT-4 时代 few-shot 优势大降（模型越强越不需要示例）——所以应该"先 zero-shot 试，行就不加示例"省成本。**System prompt 性能加成机理**：(a) 它在 final prompt 最前部（位置效应，模型对开头结尾的指令理解更好——needle in a haystack 现象）；(b) OpenAI《Instruction Hierarchy》显示模型被后训练成"system prompt 优先级最高"。**Chat template 铁律**：用错模板 = 沉默的灾难；Llama 2/3 模板不同；务必 print 出 final prompt 校验。**Context Length 真实瓶颈**：5 年内从 1K → 2M（2000 倍），但模型对长 context 中段注意力差——所以"上下文越长 ≠ 越好用"，RAG 因此仍未死。**七大最佳实践**：(1) clear instructions（评分量表、persona、examples、output format、marker）；(2) sufficient context（限制模型仅用 context）；(3) decomposition（监控/调试/并行/可写性好，但增加延迟）；(4) time to think（CoT + self-critique）；(5) iterate（一定要 version prompts + 实验追踪）；(6) tools（DSPy/OpenPrompt/Outlines/Instructor 等，但警惕 hidden API cost 与默认模板 typos）；(7) organize & version（prompts.py 分离、.prompt file、prompt catalog）。**三大攻击**：(1) prompt extraction（reverse prompt engineering 推 system prompt——"假设它迟早会公开"）；(2) jailbreaking/prompt injection（让模型做坏事或绕开规则）；(3) information extraction（泄露 context 中的隐私数据）。**关键警示**："The problem is when prompt engineering is the only thing people know"——只懂 Prompt 走不远，必须叠加 RAG/微调/评估/数据飞轮。

## §6 第6章 RAG and Agents

- **章节 UID**: 07
- **章节号**: §6
- **字数**: 17,954
- **父模块**: Prompt 与上下文
- **原文出处**: [`uid-07-RAG-and-Agents.md`](../00-原书档案/fulltext/uid-07-RAG-and-Agents.md)

> 📖 **原文**（§6.0）：Just like how a human is more likely to give a wrong answer when lacking information, AI models are more likely to make mistakes and hallucinate when they are missing context. For a given application, the model's instructions are common to all queries, whereas context is specific to each query.

> 📖 **原文**（§6.0）：Two dominating patterns for context construction are RAG, or retrieval-augmented generation, and agents. The RAG pattern allows the model to retrieve relevant information from external data sources. The agentic pattern allows the model to use tools such as web search and news APIs to gather information.

> 📖 **原文**（§6.0）：In the early days of foundation models, RAG emerged as one of the most common patterns. Its main purpose was to overcome the models' context limitations. Many people think that a sufficiently long context will be the end of RAG. I don't think so.

> 📖 **原文**（§6.0）：Context construction for foundation models is equivalent to feature engineering for classical ML models. They serve the same purpose: giving the model the necessary information to process an input.

> 📖 **原文**（§6.1 RAG 架构）：A RAG system has two components: a retriever that retrieves information from external memory sources and a generator that generates a response based on the retrieved information.

> 📖 **原文**（§6.2 检索算法）：In the literature, you might encounter the division of retrieval algorithms into the following categories: sparse versus dense. This book, however, opted for term-based versus embedding-based categorization.

> 📖 **原文**（§6.2 Term-based）：TF-IDF is an algorithm that combines these two metrics: term frequency (TF) and inverse document frequency (IDF). … Two common term-based retrieval solutions are Elasticsearch and BM25. [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25), the 25th generation of the Best Matching algorithm, was developed by Robertson et al. in the 1980s.

> 📖 **原文**（§6.2 Embedding-based）：Term-based retrieval computes relevance at a lexical level rather than a semantic level. … On the other hand, *embedding-based retrievers* aim to rank documents based on how closely their meanings align with the query.

> 📖 **原文**（§6.2 Vector Search）：Vector search is typically framed as a nearest-neighbor search problem. For large datasets, vector search is typically done using an approximate nearest neighbor (ANN) algorithm. … Some popular vector search libraries are FAISS, Google's ScaNN, Spotify's Annoy, and Hnswlib.

> 📖 **原文**（§6.2 Hybrid）：Combining term-based retrieval and embedding-based retrieval is called *hybrid search*. Different algorithms can be used in sequence. … Different algorithms can also be used in parallel as an ensemble. An algorithm for combining different rankings is called reciprocal rank fusion (RRF).

> 📖 **原文**（§6.3 优化）：Four tactics discussed here are chunking strategy, reranking, query rewriting, and contextual retrieval.

> 📖 **原文**（§6.3 Chunking）：The chunk size shouldn't exceed the maximum context length of the generative model. For the embedding-based approach, the chunk size also shouldn't exceed the embedding model''s context limit. … There is no universal best chunk size or overlap size. You have to experiment to find what works best for you.

> 📖 **原文**（§6.3 Contextual Retrieval）：Anthropic used AI models to generate a short context, usually 50-100 tokens, that explains the chunk and its relationship to the original document.

> 📖 **原文**（§6.4 Agents）：An agent is a system that uses a foundation model to interact with its environment to achieve a goal. Agents can use tools to gather information, take actions, and reflect on their progress.

> 📖 **原文**（§6.4 Tools）：Tools extend a model's capabilities beyond text generation. Common tools include web search, code interpreters, calculators, and APIs. The way a model decides which tool to use and when is called planning.

> 📖 **原文**（§6.4 Planning）：There are two main planning approaches: (1) ReAct — the model explicitly reasons about which action to take next; (2) Plan-and-Execute — the model creates a full plan upfront, then executes it step by step.

> 📖 **原文**（§6.4 Failure Modes）：Common agent failure modes include: (1) The model fails to use a tool correctly; (2) The model uses a tool when it shouldn't; (3) The model's planning gets stuck in a loop; (4) The model's plan is unachievable with available tools.

> 📖 **原文**（§6.5 Memory）：Memory in the context of agents refers to the information a model retains across multiple turns of a conversation or multiple tasks. There are three types of memory: short-term (within a single conversation), long-term (across conversations), and episodic (specific past events).

> 📖 **原文**（§6.6 评价）：The quality of a retriever should also be evaluated in the context of the whole RAG system. Ultimately, a retriever is good if it helps the system generate high-quality answers. … To summarize, the quality of a RAG system should be evaluated both component by component and end to end.

> 🧭 **归纳**：RAG 与 Agent 是"context 构造"的两大模式——前者拉数据，后者用工具。**RAG 仍无可替代**的原因：(a) 数据只增不减，长 context 总不够；(b) 模型对长 context 中段注意力差（needle in a haystack）；(c) 拉数据节省 token 费用与延迟。**RAG 架构 = retriever（indexing + querying）+ generator**；retriever 质量决定系统上限。**两大检索范式**：①**Term-based**（sparse）——TF-IDF、Elasticsearch、BM25（Best Matching 第 25 代，强 baseline）；②**Embedding-based**（dense）——语义检索，可微调但易丢关键词（特定错误码 EADDRNOTAVAIL 等）；主流用 ANN 算法（FAISS/ScaNN/Annoy/Hnswlib）做近似最近邻。**Hybrid Search** = term + embedding 组合，可串行（term 召回 → embedding 精排）或并行（RRF reciprocal rank fusion 融合排名）。**RAG 优化四大武器**：(1) **chunking**（字符/词/句子/段落/递归分块；token 分块；重叠避免边界信息丢失；越小越多 → 召回广但易丢上下文，需实验找平衡）；(2) **reranking**（粗排 → 精排，或按时间重排，对搜索位置敏感度低于传统 search）；(3) **query rewriting**（"How about Emily Doe?" → "When did Emily Doe buy..."，可用 LLM 改写，处理身份消歧）；(4) **contextual retrieval**（Anthropic 提议给每个 chunk 附 50-100 tokens 上下文，提升检索命中率）。**多模态 RAG**：retriever 返回文本 + 图像（CLIP 等多模态 embedding model 把两种 modality 映射到同一空间）；表格数据走 text-to-SQL（语义解析 + SQL 执行 + 生成）。**Agent = FM + 工具 + 规划 + 反思**；两种规划方式：**ReAct**（每步显式 reasoning → action）和 **Plan-and-Execute**（先列全 plan 再逐步执行）。**Agent 四大失败模式**：(1) 工具用错；(2) 不该用工具时用；(3) 规划死循环；(4) 目标不可达。**三种 memory**：short-term（单对话内）、long-term（跨对话）、episodic（特定事件）。**核心评估原则**：RAG 质量要"组件级 + 端到端"双评——retriever 单独评（context precision/recall）最终落到"系统能否产生好答案"。