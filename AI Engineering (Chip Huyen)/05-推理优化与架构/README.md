# 五 推理优化与架构（§9-§10）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

## §9 第9章 Inference Optimization

- **章节 UID**: 10
- **章节号**: §9
- **字数**: 13,649
- **父模块**: 推理优化与架构
- **原文出处**: [`uid-10-Inference-Optimization.md`](../00-原书档案/fulltext/uid-10-Inference-Optimization.md)

> 📖 **原文**（§9.0）：Inference optimization can be done at the model, hardware, and service levels. At the model level, you can reduce a trained model's size or develop more efficient architectures. At the hardware level, you can design more powerful hardware.

> 📖 **原文**（§9.0）：Sometimes, a technique that speeds up a model can also reduce its cost. For example, reducing a model's precision makes it smaller and faster. But often, optimization requires trade-offs. For example, the best hardware might make your model run faster but at a higher cost.

> 📖 **原文**（§9.1 推理两阶段）：Recall from Chapter 2 that inference for a transformer-based language model consists of two steps, prefilling and decoding: Prefill — The model processes the input tokens in parallel. How many tokens can be processed at once is limited by the number of operations your hardware can execute in a given time. Therefore, prefilling is *compute-bound*. Decode — The model generates one output token at a time. … Decoding is, therefore, *memory bandwidth-bound*.

> 📖 **原文**（§9.1）：Different model architectures and workloads result in different computational bottlenecks. For example, inference for image generators like Stable Diffusion is typically compute-bound, whereas inference for autoregression language models is typically memory bandwidth-bound.

> 📖 **原文**（§9.1 Online vs Batch）：Online APIs optimize for latency. … Batch APIs optimize for cost. If your application doesn't have strict latency requirements, you can send them to batch APIs for more efficient processing. Higher latency allows a broader range of optimization techniques, including batching requests together and using cheaper hardware. For example, as of this writing, both Google Gemini and OpenAI offer batch APIs at a 50% cost reduction and significantly higher turnaround time.

> 📖 **原文**（§9.2 延迟指标）：Latency measures the time from when users send a query until they receive the complete response. For autoregressive generation, especially in the streaming mode, the overall latency can be broken into several metrics: Time to first token (TTFT) · Time per output token (TPOT) · Time between tokens (TBT).

> 📖 **原文**（§9.2）：In the streaming mode, where users read each token as it's generated, TPOT should be faster than human reading speed but doesn't have to be much faster. A very fast reader can read 120 ms/token, so a TPOT of around 120 ms, or 6–8 tokens/second, is sufficient for most use cases.

> 📖 **原文**（§9.2 Goodput）：Goodput measures the number of requests per second that satisfies the SLO, software-level objective. … Due to this trade-off, focusing on an inference service based solely on its throughput and cost can lead to a bad user experience.

> 📖 **原文**（§9.2 MFU/MBU）：MFU is the ratio of the observed throughput (tokens/s) relative to the theoretical maximum throughput of a system operating at peak FLOP/s. … MBU (Model Bandwidth Utilization) measures the percentage of achievable memory bandwidth used.

> 📖 **原文**（§9.2）：What's considered a good MFU and MBU depends on the model, hardware, and workload. Compute-bound workloads typically have higher MFU and lower MBU, while bandwidth-bound workloads often show lower MFU and higher MBU.

> 📖 **原文**（§9.3 硬件）：The main difference between CPUs and GPUs is that CPUs are designed for general-purpose usage, whereas GPUs are designed for parallel processing: CPUs have a few powerful cores, typically up to 64 cores for high-end consumer machines. … GPUs have thousands of smaller, less powerful cores optimized for tasks that can be broken down into many smaller, independent calculations.

> 📖 **原文**（§9.3）：Inference can exceed the cost of training in commonly used systems, and that inference accounts for up to 90% of the machine learning costs for deployed AI systems.

> 📖 **原文**（§9.4 模型优化）：Model optimization techniques include: (1) Quantization — reducing numerical precision to lower memory and accelerate computation; (2) Distillation — training a smaller model to mimic a larger one; (3) Pruning — removing less important weights or neurons; (4) Architecture search — finding more efficient architectures.

> 📖 **原文**（§9.4 量化与推理）：Quantization at inference is simpler than at training because there's no backward pass to worry about. Common inference quantization: FP32 → FP16/BF16 (2x memory reduction, minimal accuracy loss); FP16 → INT8 (4x memory reduction, mild accuracy loss); INT8 → INT4 (8x memory reduction, more accuracy loss).

> 📖 **原文**（§9.5 服务优化）：Inference service optimization techniques include: Batching · KV caching · Prompt caching · Speculative decoding · Continuous batching.

> 📖 **原文**（§9.5 KV Cache）：KV caching stores the key and value vectors computed during prefilling so they can be reused during decoding. Without KV caching, each new token would require recomputing all previous tokens' key and value vectors, which is O(n²) per token. With KV caching, this becomes O(n) per token.

> 📖 **原文**（§9.5 Speculative Decoding）：Speculative decoding uses a small draft model to generate several tokens quickly, then verifies them with the large model in a single forward pass. If the draft is correct, you get multiple tokens in the time of one. If wrong, you fall back to the large model's output for that position.

> 📖 **原文**（§9.5 Continuous Batching）：Continuous batching (also called in-flight batching) processes new requests as soon as a slot frees up, rather than waiting for all requests in a batch to finish. This dramatically improves GPU utilization and reduces the average latency for individual requests.

> 🧭 **归纳**：FM 推理优化横跨模型/硬件/服务三层。**推理两阶段是优化一切的总开关**——**Prefill**（并行处理输入 tokens，compute-bound）+ **Decode**（逐 token 生成，memory bandwidth-bound）——这意味着：(a) 两阶段在不同机器上跑（prefill 机器 vs decode 机器）已是生产常态；(b) 长 context 偏 memory-bound，短 prompt 偏 compute-bound。**Online API vs Batch API** = 延迟优先 vs 成本优先（OpenAI/Gemini batch API 半价但分钟级到小时级）；适合 batch 的场景：合成数据生成、定时报表、新客户 onboarding、模型迁移、推荐刷新、知识库重建。**推理度量五件套**——**TTFT**（time to first token，prefill 阶段时间，用户等待首字时常感知为"卡不卡"）、**TPOT**（time per output token，decode 阶段每字时间，120ms/字 ≈ 8 token/秒 足够人眼阅读速度）、**TBT/ITL**（time between tokens）、**Throughput**（输出 token/秒 + 输入 token/秒分开算）、**Goodput**（满足 SLO 的 RPS，"达到延迟目标的有效吞吐量"）。**MFU/MBU** 比 NVIDIA 官方 GPU utilization 更准——前者看算力利用率，后者看带宽利用率。**硬件**：CPU 通用少量强核 vs GPU 大量弱核并行（矩阵乘法完美匹配），所以 AlexNet 之后 GPU 成主流；inference 占 ML 总成本高达 90%（vs 训练），所以专用 inference chip（AWS Inferentia / Apple Neural Engine / MTIA / Edge TPU / Jetson）涌现。**模型优化四件套**：Quantization（FP32→FP16→INT8→INT4）、Distillation（学生模型学教师 logits）、Pruning（剪枝）、Architecture Search（更高效架构）。**服务优化五大金刚**：(1) **Batching**（GPU 利用率 ↑，延迟 ↑）；(2) **KV Cache**（decode 时把 K/V 存下来，每 token 从 O(n²) 降到 O(n)）；(3) **Prompt Cache**（重复 prompt 段跨请求复用）；(4) **Speculative Decoding**（小模型先草拟 → 大模型一次 verify，可一次出多 token）；(5) **Continuous Batching**（slot 空出来立即填新请求，告别"凑满 batch 等最慢那个"）。**关键提醒**：latency/throughput 是天然 trade-off——技术可以 double throughput，但以牺牲 TTFT/TPOT 为代价；盯着"高 utilization"没意义，要盯着"用户花了多少钱等多久拿到了回答"。

## §10 第10章 AI Engineering Architecture and User Feedback

- **章节 UID**: 11
- **章节号**: §10
- **字数**: 13,219
- **父模块**: 推理优化与架构
- **原文出处**: [`uid-11-AI-Engineering-Architecture-and-User-Feedback.md`](../00-原书档案/fulltext/uid-11-AI-Engineering-Architecture-and-User-Feedback.md)

> 📖 **原文**（§10.0）：Given the wide range of AI engineering techniques and tools available, selecting the right ones can feel overwhelming. To simplify this process, this chapter takes a gradual approach. It starts with the simplest architecture for a foundation model application, highlights the challenges of that architecture, and gradually adds components to address them.

> 📖 **原文**（§10.0）：User feedback has always been invaluable for guiding product development, but for AI applications, user feedback has an even more crucial role as a data source for improving models. The conversational interface makes it easier for users to give feedback but harder for developers to extract signals.

> 📖 **原文**（§10.1 Step 1）：The initial expansion of a platform usually involves adding mechanisms to allow the system to construct the relevant context needed by the model to answer each query.

> 📖 **原文**（§10.1）：Context construction is like feature engineering for foundation models. It gives the model the necessary information to produce an output.

> 📖 **原文**（§10.2 Input Guardrails）：Input guardrails typically protect against two types of risks: leaking private information to external APIs and executing bad prompts that compromise your system.

> 📖 **原文**（§10.2 PII 保护）：Many sensitive data detection tools use AI to identify potentially sensitive information, such as determining if a string resembles a valid home address. If a query is found to contain sensitive information, you have two options: block the entire query or remove the sensitive information from it. For instance, you can mask a user's phone number with the placeholder [PHONE NUMBER].

> 📖 **原文**（§10.2 Output Guardrails）：A model can fail in many different ways. Output guardrails have two main functions: (1) Catch output failures; (2) Specify the policy to handle different failure modes.

> 📖 **原文**（§10.2 失败兜底）：Many failures can be mitigated by simple retry logic. AI models are probabilistic, which means that if you try a query again, you might get a different response. … It's also common to fall back on humans for tricky requests.

> 📖 **原文**（§10.2 Guardrail 工具）：Guardrail solutions that you can use out of the box include Meta's Purple Llama, NVIDIA's NeMo Guardrails, Azure's PyRIT, Azure's AI content filters, the Perspective API, and OpenAI's content moderation API.

> 📖 **原文**（§10.3 Router）：Instead of using one model for all queries, you can have different solutions for different types of queries. … A router typically consists of *an intent classifier* that predicts what the user is trying to do.

> 📖 **原文**（§10.3 Gateway）：A model gateway is an intermediate layer that allows your organization to interface with different models in a unified and secure manner. The most basic functionality of a model gateway is to provide a unified interface to different models.

> 📖 **原文**（§10.3 Gateway 功能）：A model gateway provides *access control and cost management*. Instead of giving everyone who wants access to the OpenAI API your organizational tokens, which can be easily leaked, you give people access only to the model gateway.

> 📖 **原文**（§10.4 Cache）：In general, there are two major system caching mechanisms: exact caching and semantic caching.

> 📖 **原文**（§10.4 Exact Cache）：With exact caching, cached items are used only when these exact items are requested. … Caching, when not properly handled, can cause data leaks. Imagine you work for an ecommerce site, and user X asks a seemingly generic question such as: "What is the return policy for electronics products?" … Mistaking this query for a generic question, the system caches the answer. Later, when user Y asks the same question, the cached result is returned, revealing X's information to Y.

> 📖 **原文**（§10.4 Semantic Cache）：Unlike in exact caching, cached items are used even if they are only semantically similar, not identical, to the incoming query. … Semantic cache might still be worthwhile if the cache hit rate is high, meaning that a good portion of queries can be effectively answered by leveraging the cached results.

> 📖 **原文**（§10.5 Step 5 Agent）：As discussed in Chapter 6, an application flow can be more complex with loops, parallel execution, and conditional branching. Agentic patterns can help you build complex applications.

> 📖 **原文**（§10.5 Write Actions）：A model's outputs also can be used to invoke write actions, such as composing an email, placing an order, or initializing a bank transfer. Write actions allow a system to make changes to its environment directly. Write actions can make a system vastly more capable but also expose it to significantly more risks. Giving a model access to write actions should be done with the utmost care.

> 📖 **原文**（§10.6 Monitoring）：Three metrics can help evaluate the quality of your system's observability, derived from the DevOps community: MTTD (mean time to detection) · MTTR (mean time to response) · CFR (change failure rate).

> 📖 **原文**（§10.6）：Having a high CFR doesn't necessarily indicate a bad monitoring system. However, you should rethink your evaluation pipeline so that bad changes are caught before being deployed. Evaluation and monitoring need to work closely together.

> 📖 **原文**（§10.6 用户反馈）：User feedback can be explicit (thumbs up/down, ratings) or implicit (regenerating a response, copying a response, abandoning a conversation). Implicit feedback is more abundant but harder to interpret.

> 📖 **原文**（§10.7 Orchestration）：AI pipeline orchestration coordinates the execution of multiple components in an AI application, handling data flow, error handling, and state management. Common orchestration frameworks include LangChain, LlamaIndex, and Haystack. However, these frameworks can add complexity, so evaluate carefully whether you need them.

> 🧭 **归纳**：第 10 章把全书串成"渐进式生产架构"——从最简单的"query → 模型 → 响应"逐步加组件，每加一层解决一类问题。**五步走**——**Step 1 Enhance Context**：加 RAG、tool use、multimodal retrieval（"context construction 是 foundation model 的 feature engineering"）。**Step 2 Guardrails**：input 端防 PII 泄露（用 AI 识别敏感数据 + placeholder 屏蔽 + reverse PII map 解掩；防 prompt injection/jailbreak）；output 端抓失败（empty response / 格式错 / 事实幻觉 / 有害内容）+ 兜底（retry、用 AI 判官重生成、转人工）。**Step 3 Router + Gateway**：Router = intent classifier 把 query 分到不同模型/agent/FAQ/人工（防 out-of-scope 省 API call）；Gateway = 统一接口 + access control + cost cap + fallback policy + load balancing（Portkey、MLflow、TrueFoundry、Kong 等开箱即用）。**Step 4 Cache**：exact cache 强一致但命中率低；semantic cache 命中率高但易引入数据泄露（PII 跨用户共享）+ 阈值难调；vector DB 存 query embeddings；personal/time-sensitive query 别 cache。**Step 5 Agent Patterns**：loop + parallel execution + conditional branching + write actions（agent 调外部工具改环境 = 能力 ↑ 但风险 ↑）。**监控三件套 (DevOps 转译)**：MTTD (mean time to detection) + MTTR (mean time to response) + CFR (change failure rate)——CFR 高说明监控不够。**评估 ↔ 监控必须互通**：评估指标是监控指标的子集，监控发现的坏 case 反馈到评估。**User Feedback 两类**：explicit（thumbs up/down、评分）vs implicit（重新生成、复制回答、放弃对话）；implicit 多但难解——对话界面让用户更容易给反馈但让开发者更难提取信号。**Orchestration 框架**（LangChain / LlamaIndex / Haystack）能管理多组件协同 + 数据流 +状态，但加复杂度——先用朴素代码，需要时再上框架。**核心心智模型**：架构渐进生长（从 query→model 到 query→context→guard→router→gateway→cache→agent），不要 over-engineer 一次到位；用户反馈是 AI 应用最关键的数据源（数据飞轮的发动机）。