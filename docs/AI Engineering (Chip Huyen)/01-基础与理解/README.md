# 一 基础与理解（Preface + §1-§2）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

## Preface 前言

- **章节 UID**: 01
- **章节号**: 前言
- **字数**: 3,944
- **父模块**: 基础与理解
- **原文出处**: [`uid-01-Preface.md`](../00-原书档案/fulltext/uid-01-Preface.md)

> 📖 **原文**：This book covers the end-to-end process of adapting foundation models to solve real-world problems, encompassing tried-and-true techniques from other engineering fields and techniques emerging with foundation models.

> 📖 **原文**：This book provides a framework for adapting foundation models, which include both large language models (LLMs) and large multimodal models (LMMs), to specific applications.

> 📖 **原文**：AIE can be a companion to DMLS. DMLS focuses on building applications on top of traditional ML models, which involves more tabular data annotations, feature engineering, and model training. AIE focuses on building applications on top of foundation models, which involves more prompt engineering, context construction, and parameter-efficient finetuning.

> 📖 **原文**：This book is for anyone who wants to leverage foundation models to solve real-world problems. This is a technical book, so the language of this book is geared toward technical roles, including AI engineers, ML engineers, data scientists, engineering managers, and technical product managers.

> 📖 **原文**：This book is structured to follow the typical process for developing an AI application. … Because this book is modular, you're welcome to skip any section that you're already familiar with or that is less relevant to you.

> 🧭 **归纳**：前言用 11 道问答锁定本书射程——该不该做这个 AI 应用？怎么评估？幻觉成因？Prompt 最佳实践？RAG 工作机理？Agent 怎么搭？何时/何时不微调？数据量与质量怎么定？如何让模型更快更便宜？如何搭反馈循环？全书结构按"AI 应用开发的典型流程"展开（评估→提示→RAG/Agent→微调→数据→推理→架构），且与姊妹书 DMLS（Designing Machine Learning Systems）形成"传统 ML vs Foundation Model"的并列：传统 ML 重 tabular 数据标注/特征工程/模型训练；AIE 重 Prompt/上下文/PEFT。每个章节可独立跳过，但骨架是"端到端流程 + 评估驱动"。

## §1 第1章 Introduction to Building AI Applications with Foundation Models

- **章节 UID**: 02
- **章节号**: §1
- **字数**: 15,736
- **父模块**: 基础与理解
- **原文出处**: [`uid-02-Introduction-to-Building-AI-Applications-with-Foundation-Models.md`](../00-原书档案/fulltext/uid-02-Introduction-to-Building-AI-Applications-with-Foundation-Models.md)

> 📖 **原文**（§1.0）：The scaling up of AI models has two major consequences. First, AI models are becoming more powerful and capable of more tasks, enabling more applications. … Second, training large language models (LLMs) requires data, compute resources, and specialized talent that only a few organizations can afford. This has led to the emergence of *model as a service*.

> 📖 **原文**（§1.0）：In short, the demand for AI applications has increased while the barrier to entry for building AI applications has decreased. This has turned *AI engineering*—the process of building applications on top of readily available models—into one of the fastest-growing engineering disciplines.

> 📖 **原文**（§1.1 上升史）：While language models have been around for a while, they've only been able to grow to the scale they are today with *self-supervision.* … Language modeling is self-supervised because each input sequence provides both the labels (tokens to be predicted) and the contexts the model can use to predict these labels.

> 📖 **原文**（§1.1）：There are two main types of language models: *masked language models* and *autoregressive language models*. … An autoregressive language model is trained to predict the next token in a sequence, *using only the preceding tokens*. … Today, autoregressive language models are the models of choice for text generation, and for this reason, they are much more popular than masked language models.

> 📖 **原文**（§1.1）：The basic unit of a language model is *token*. A token can be a character, a word, or a part of a word (like -tion), depending on the model. … For GPT-4, an average token is approximately [¾ the length of a word]. So, 100 tokens are approximately 75 words.

> 📖 **原文**（§1.1 上升史 - LLM to FM）：While many people still call Gemini and GPT-4V LLMs, they're better characterized as [*foundation models*](https://arxiv.org/abs/2108.07258). The word *foundation* signifies both the importance of these models in AI applications and the fact that they can be built upon for different needs.

> 📖 **原文**（§1.2 用例）：Prompt engineering, RAG, and finetuning are three very common AI engineering techniques that you can use to adapt a model to your needs. The rest of the book will discuss all of them in detail.

> 📖 **原文**（§1.3 AI 工程崛起三因素）：The availability and accessibility of powerful foundation models lead to three factors that, together, create ideal conditions for the rapid growth of AI engineering as a discipline: (1) General-purpose AI capabilities; (2) Increased AI investments; (3) Low entrance barrier to building AI applications.

> 📖 **原文**（§1.3）：*Anyone, and I mean anyone, can now develop AI applications.*

> 📖 **原文**（§1.3 用例 8 类）：I categorized applications into eight groups [Table 1-3]: Coding · Image and video production · Writing · Education · Conversational bots · Information aggregation · Data organization · Workflow automation.

> 📖 **原文**（§1.4 AI 工程栈）：The AI stack consists of three layers from the bottom up: (1) the infrastructure layer (NVIDIA, AWS, etc.); (2) the model layer (OpenAI, Anthropic, etc.); (3) the application layer (companies building applications for end users).

> 📖 **原文**（§1.4）：AI engineering focuses on building applications on top of foundation models, while ML engineering focuses on building models. … AI engineering is application development. ML engineering is model development. The roles of an AI engineer and an ML engineer have different focus areas, but the underlying skills significantly overlap.

> 🧭 **归纳**：本章把 AI 工程立为独立学科而非 ML 工程的延伸。三件事的同步发生催生了它：①模型规模化让能力涌现（语言模型→LLM→FM，多模态成为标配）；②训练 FM 所需的数据/算力/人才只向少数巨头开放（Google、Meta、OpenAI、Anthropic），催生"model as a service"商业形态；③API + ChatGPT 级别 UX 把准入门槛降到普通人。**术语共识**：Foundation Model 涵盖 LLM 和 LMM；自监督让语言模型可吃下互联网级数据；token 是基本单位（GPT-4 ≈ 100 tokens = 75 词）；自回归 LM 因文本生成场景成为主流。**三大适配技术**：Prompt Engineering（不改权重）、RAG（外挂上下文）、Finetuning（改权重）——后续 10 章全部围绕这三者展开。**AI 工程栈三层**：基础设施（NVIDIA/AWS）→ 模型（OpenAI/Anthropic）→ 应用层。**AI 工程师 vs ML 工程师**：前者开发应用、后者开发模型，但底层技能大量重叠。**AI 工程不是银弹**：适合需求明确、评估可量化、有数据飞轮的应用；本章结尾的 8 大用例（Coding / 图像视频 / 写作 / 教育 / 对话 bot / 信息聚合 / 数据组织 / 工作流自动化）就是"FM 擅长"的高 ROI 起点。

## §2 第2章 Understanding Foundation Models

- **章节 UID**: 03
- **章节号**: §2
- **字数**: 19,938
- **父模块**: 基础与理解
- **原文出处**: [`uid-03-Understanding-Foundation-Models.md`](../00-原书档案/fulltext/uid-03-Understanding-Foundation-Models.md)

> 📖 **原文**（§2.1 数据）：An AI model is only as good as the data it was trained on. If there's no Vietnamese in the training data, the model won't be able to translate from English into Vietnamese. Similarly, if an image classification model sees only animals in its training set, it won't perform well on photos of plants.

> 📖 **原文**（§2.1）：English dominates the internet. An analysis of the Common Crawl dataset shows that English accounts for almost half of the data (45.88%), making it eight times more prevalent than the second-most common language, Russian (5.97%). … Languages with limited availability as training data—typically languages not included in this list—are considered *low-resource*.

> 📖 **原文**（§2.1）：Given that LLMs are generally good at translation, can we just translate all queries from other languages into English, obtain the responses, and translate them back into the original language? Many people indeed follow this approach, but it's not ideal. First, this requires a model that can sufficiently understand under-represented languages to translate. Second, translation can cause information loss.

> 📖 **原文**（§2.2 架构）：As of this writing, the most dominant architecture for language-based foundation models is the *transformer* architecture (Vaswani et al., 2017), which is based on the attention mechanism.

> 📖 **原文**（§2.2）：The transformer architecture addresses both [seq2seq] problems with the attention mechanism. The attention mechanism allows the model to weigh the importance of different input tokens when generating each output token.

> 📖 **原文**（§2.2 推理两阶段）：Inference for transformer-based language models, therefore, consists of two steps: (1) Prefill — the model processes the input tokens in parallel; (2) Decode — the model generates one output token at a time.

> 📖 **原文**（§2.2 替代架构）：One popular model is RWKV (Peng et al., 2023), an RNN-based model that can be parallelized for training. … An architecture that has shown a lot of promise in long-range memory is SSMs (state space models). … Mamba scales SSMs to three billion parameters. … Jamba interleaves blocks of transformer and Mamba layers to scale up SSMs even further.

> 📖 **原文**（§2.3 模型规模）：In general, increasing a model's parameters increases its capacity to learn, resulting in better models. … A type of sparse model that has gained popularity in recent years is mixture-of-experts (MoE). An MoE model is divided into different groups of parameters, and each group is an *expert*. Only a subset of the experts is *active* for (used to) process each token.

> 📖 **原文**（§2.3 缩放律）：Given a compute budget, the rule that helps calculate the optimal model size and dataset size is called the Chinchilla *scaling law*, proposed in the Chinchilla paper. … for compute-optimal training, you need the number of training tokens to be approximately 20 times the model size.

> 📖 **原文**（§2.3）：*Three numbers signal a model's scale*: number of parameters (proxy for learning capacity); number of tokens a model was trained on (proxy for how much a model learned); number of FLOPs (proxy for the training cost).

> 📖 **原文**（§2.4 后训练）：A model can also be finetuned with reinforcement learning to generate responses that maximize human preference. Preference finetuning requires comparative data that typically follows the format (instruction, winning response, losing response).

> 📖 **原文**（§2.5 采样）：Sampling is how a model chooses an output from all possible options. It is perhaps one of the most underrated concepts in AI. Not only does sampling explain many seemingly baffling AI behaviors, including hallucinations and inconsistencies, but choosing the right sampling strategy can also significantly boost a model's performance with relatively little effort.

> 📖 **原文**（§2.5）：The outputs of language models are open-ended. A language model can use its fixed, finite vocabulary to construct infinite possible outputs. A model that can generate open-ended outputs is called *generative*, hence the term *generative AI*.

> 📖 **原文**（§2.5）：Structured outputs, such as JSON, YAML, or regex, constrain a model's output to follow a specific format. Many model APIs support this via schema-guided generation (e.g., OpenAI's structured output, Anthropic's tool use with JSON schema). … Constraining outputs is essential for production systems where downstream code expects a specific format.

> 🧭 **归纳**：本章把"FM 是什么"拆成五个下层决策，每个决策都直接决定下游应用表现：**①训练数据** = "use what we have, not what we want"——Common Crawl 噪音大、英语占 45.88%，低资源语言（Telugu/Marathi/Punjabi）质量差；语言结构与 tokenization 效率也让 Burmese 等语言推理慢 10 倍、贵 10 倍。**②模型架构** = Transformer 仍是绝对主流（attention 让并行输入、串行输出成为可能；推理两阶段 prefill + decode 是后续所有优化技术的隐线），但替代架构（Mamba 的线性时间序列建模、Jamba 的 Transformer+Mamba 混合、RWKV 的 RNN+可并行训练）正挑战其"上下文长度无法扩展"的局限。**③模型规模** = 参数数 ≠ 实际推理成本（MoE 的 Mixtral 8x7B 有 46.7B 参数但每 token 只激活 12.9B）；缩放律（Chinchilla）告诉你给固定算力预算，模型大小与训练 token 应"等比例翻倍"；稀疏模型（≥90% 0 值参数）让"大模型低成本"成为可能。**④后训练** = SFT（监督指令微调）+ Preference Finetuning（RLHF 等偏好对齐）把"能预测下一个 token"变成"按人类偏好回答问题"。**⑤采样** = "被严重低估的概念"——同一 prompt 多次采样可得到不同输出；温度、top-p、top-k 是三个最常用旋钮；结构化输出（JSON/YAML/regex）是生产系统"代码下游可用"的硬要求；这能解释幻觉、重复、不一致等"看似奇葩"的行为。**为什么这章重要**：选模型时不知道训练数据来源、架构、规模、后训练，就只能盲选；做 Prompt 调优时不知道采样策略，就解释不了"为啥同一 prompt 多次跑结果不同"。本章是全书所有"为什么这能做/不能做"的根。