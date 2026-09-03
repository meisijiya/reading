# 二 评估方法（§3-§4）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

## §3 第3章 Evaluation Methodology

- **章节 UID**: 04
- **章节号**: §3
- **字数**: 15,600
- **父模块**: 评估方法
- **原文出处**: [`uid-04-Evaluation-Methodology.md`](../00-原书档案/fulltext/uid-04-Evaluation-Methodology.md)

> 📖 **原文**（§3.0）：For some applications, figuring out evaluation can take up the majority of the development effort.

> 📖 **原文**（§3.1 评估为何难）：First, the more intelligent AI models become, the harder it is to evaluate them. … Second, the open-ended nature of foundation models undermines the traditional approach of evaluating a model against ground truths. … Third, most foundation models are treated as black boxes. … Last but not least, the scope of evaluation has expanded for general-purpose models.

> 📖 **原文**（§3.1）：publicly available evaluation benchmarks have proven to be inadequate for evaluating foundation models. … A benchmark becomes saturated for a model once the model achieves the perfect score. With foundation models, benchmarks are becoming saturated fast. … MMLU (2020) was largely replaced by MMLU-Pro (2024).

> 📖 **原文**（§3.2 LM 度量）：Most autoregressive language models are trained using cross entropy or its relative, perplexity. When reading papers and model reports, you might also come across bits-per-character (BPC) and bits-per-byte (BPB); both are variations of cross entropy.

> 📖 **原文**（§3.2）：*Entropy* measures how much information, on average, a token carries. The higher the entropy, the more information each token carries, and the more bits are needed to represent a token.

> 📖 **原文**（§3.2）：If the language model learns perfectly from its training data, the model's cross entropy will be exactly the same as the entropy of the training data. The KL divergence of Q with respect to P will then be 0. You can think of a model's cross entropy as its approximation of the entropy of its training data.

> 📖 **原文**（§3.2 Perplexity 解读）：The perplexity of a language model (with the learned distribution *Q*) on this dataset is defined as: PPL(P, Q) = 2^H(P, Q). If cross entropy measures how difficult it is for a model to predict the next token, perplexity measures the amount of uncertainty it has when predicting the next token.

> 📖 **原文**（§3.2）：*What's considered a good value for perplexity depends on the data itself and how exactly perplexity is computed*. More structured data gives lower expected perplexity. The bigger the vocabulary, the higher the perplexity. The longer the context length, the lower the perplexity.

> 📖 **原文**（§3.2）：*Perplexity can be used to detect whether a text was in a model's training data.* This is useful for detecting data contamination—if a model's perplexity on a benchmark's data is low, this benchmark was likely included in the model's training data.

> 📖 **原文**（§3.3 精确评估）：When evaluating models' performance, it's important to differentiate between exact and subjective evaluation. Exact evaluation produces judgment without ambiguity. … AI as a judge is subjective. The evaluation result can change based on the judge model and the prompt.

> 📖 **原文**（§3.3 Functional Correctness）：Code generation is an example of a task where functional correctness measurement can be automated. Functional correctness in coding is sometimes *execution accuracy*. … Popular benchmarks for evaluating AI's code generation capabilities, such as OpenAI's HumanEval and Google's MBPP (Mostly Basic Python Problems Dataset) use functional correctness as their metrics.

> 📖 **原文**（§3.3 Pass@k）：When evaluating a model, for each problem a number of code samples, denoted as *k*, are generated. A model solves a problem if any of the *k* code samples it generated pass all of that problem's test cases. The final score, called *pass@k*, is the fraction of the solved problems out of all problems.

> 📖 **原文**（§3.3 Lexical Similarity）：Common metrics for lexical similarity are BLEU, ROUGE, METEOR++, TER, and CIDEr. They differ in exactly how the overlapping is calculated. … Since the rise of foundation models, fewer benchmarks use lexical similarity.

> 📖 **原文**（§3.3 Semantic Similarity）：Semantic similarity aims to compute the similarity in semantics. This first requires transforming a text into a numerical representation, which is called an *embedding*. … Semantic similarity can be computed for embeddings of any data modality, including images and audio. Semantic similarity for text is sometimes called semantic textual similarity.

> 📖 **原文**（§3.4 AI as Judge）：The approach of using AI to evaluate AI is called AI as a judge or LLM as a judge. An AI model that is used to evaluate other AI models is called an *AI judge*. … As of this writing, AI as a judge has become one of the most, if not the most, common methods for evaluating AI models in production. … LangChain's *State of AI* report in 2023 noted that 58% of evaluations on their platform were done by AI judges.

> 📖 **原文**（§3.5 Comparative Eval）：Comparative evaluation, in which an AI judge is asked to rank a pair of model outputs, is gaining traction. The most prominent example is the Chatbot Arena's leaderboard, which uses Elo scores derived from millions of pairwise comparisons.

> 🧭 **归纳**：评估是 AI 工程的瓶颈，且无捷径。**为何难**：①模型越强越难评（PhD 级解题非普通人能判）；②开放性输出无 ground truth（同一问有无穷多正确答案）；③大多数 FM 是黑盒（架构/训练数据/过程不公开）；④评估边界已扩展（从"做已知任务"到"发现能做的新任务"）；⑤公开 benchmark 快速饱和（GLUE→SuperGLUE→MMLU→MMLU-Pro 不断换）。**评估方法论四大金刚**——**①LM 度量**（entropy/cross entropy/BPC/BPB/perplexity，PPL=2^H）：可用作数据污染检测（某文本在训练集→PPL 异常低）、能力代理（PPL 与下游表现强相关）、去重门槛；缺点：post-training 后 PPL 不再单调反映能力。**②精确评估**（functional correctness / 相似度 / embedding）：代码用 HumanEval pass@k（k 样本数）；text-to-SQL 用 Spider/BIRD；BLEU/ROUGE 仍是翻译/摘要的传统指标但已少用；semantic similarity 用 cosine similarity on embeddings，跨模态可用（CLIP）。**③AI as Judge**——LMSYS 数据显示 58% 生产评估走这条路；优势：scalable、便宜、可解释（LLM 给 reasoning）；缺点：主观（判官不同分不同）、有偏见（位置偏好/长度偏好/自我偏好）。**④Comparative Eval**——让 AI 评判两个输出哪个好，最成功案例是 Chatbot Arena 的 Elo 排行榜。**总入口**：没有评估别往下走；先看 §3.3 精确评估能用就用，§3.4 AI 判官处理主观项，最后 §4 章把它拼成 pipeline。

## §4 第4章 Evaluate AI Systems

- **章节 UID**: 05
- **章节号**: §4
- **字数**: 18,880
- **父模块**: 评估方法
- **原文出处**: [`uid-05-Evaluate-AI-Systems.md`](../00-原书档案/fulltext/uid-05-Evaluate-AI-Systems.md)

> 📖 **原文**（§4.0）：An application that is deployed but can't be evaluated is worse. It costs to maintain, but if you want to take it down, it might cost even more. … I call this approach *evaluation-driven development*. The name is inspired by test-driven development.

> 📖 **原文**（§4.0）：While some companies chase the latest hype, sensible business decisions are still being made based on returns on investment, not hype. Applications should demonstrate value to be deployed. … I believe that evaluation is the biggest bottleneck to AI adoption.

> 📖 **原文**（§4.1 评估四桶）：In general, you can think of criteria in the following buckets: domain-specific capability, generation capability, instruction-following capability, and cost and latency.

> 📖 **原文**（§4.1 领域能力）：Domain-specific capabilities are commonly evaluated using exact evaluation. Coding-related capabilities are typically evaluated using functional correctness. … Efficiency can be exactly evaluated by measuring runtime or memory usage.

> 📖 **原文**（§4.1 MCQ）：Here's an example of a multiple-choice question in the MMLU benchmark: … A drawback of using MCQs is that a model's performance on MCQs can vary with small changes in how the questions and the options are presented. … MCQs are best suited for evaluating knowledge and reasoning. They aren't ideal for evaluating generation capabilities such as summarization, translation, and essay writing.

> 📖 **原文**（§4.1 事实一致性）：Local factual consistency — The output is evaluated against a context. … Global factual consistency — The output is evaluated against open knowledge.

> 📖 **原文**（§4.1 事实一致性）：SelfCheckGPT relies on an assumption that if a model generates multiple outputs that disagree with one another, the original output is likely hallucinated. Given a response R to evaluate, SelfCheckGPT generates N new responses and measures how consistent R is with respect to these N new responses.

> 📖 **原文**（§4.1 事实一致性）：SAFE, Search-Augmented Factuality Evaluator, introduced by Google DeepMind (Wei et al., 2024). … SAFE breaks an output into individual facts and then uses a search engine to verify each fact.

> 📖 **原文**（§4.1 Safety）：It's possible to use general-purpose AI judges to detect these scenarios, and many people do. GPTs, Claude, and Gemini can detect many harmful outputs if prompted properly. … Examples of these models are Facebook's hate speech detection model, the Skolkovo Institute's toxicity classifier, and Perspective API.

> 📖 **原文**（§4.1 Instruction Following）：More powerful models are generally better at following instructions. GPT-4 is better at following most instructions than GPT-3.5. … You should curate your own benchmark to evaluate your model's capability to follow your instructions using your own criteria.

> 📖 **原文**（§4.1 成本延迟）：A model that generates high-quality outputs but is too slow and expensive to run will not be useful. When evaluating models, it's important to balance model quality, latency, and cost. Many companies opt for lower-quality models if they provide better cost and latency.

> 📖 **原文**（§4.1 成本延迟）：When optimizing for multiple objectives, it's important to be clear about what objectives you can and can't compromise on. For example, if latency is something you can't compromise on, you start with latency expectations for different models, filter out all the models that don't meet your latency requirements, and then pick the best among the rest.

> 📖 **原文**（§4.2 Model Selection）：When looking at models, it's important to differentiate between hard attributes (what is impossible or impractical for you to change) and soft attributes (what you can and are willing to change). Hard attributes are often the results of decisions made by model providers (licenses, training data, model size) or your own policies (privacy, control).

> 📖 **原文**（§4.2 Model Selection 工作流）：At a high level, the evaluation workflow consists of four steps: (1) Filter out models whose hard attributes don't work for you. (2) Use publicly available information, e.g., benchmark performance and leaderboard ranking, to narrow down the most promising models. (3) Run experiments with your own evaluation pipeline to find the best model. (4) Continually monitor your model in production to detect failure and collect feedback to improve your application.

> 📖 **原文**（§4.2 Build vs Buy）：A question many teams will need to visit over and over again is whether to host their own models or to use a model API. This question has become more nuanced with the introduction of model API services built on top of open source models.

> 📖 **原文**（§4.3 Eval Pipeline）：The last part discusses developing an evaluation pipeline that can guide the development of your application over time. … Step 1. Evaluate All Components in a System. Step 2. Create an Evaluation Guideline. Step 3. Define Evaluation Methods and Data.

> 🧭 **归纳**：第 4 章把第 3 章的方法论装配成生产级评估体系。**核心主张**：①**评估驱动开发（EDD）**——评估之于 AI 工程 = TDD 之于软件工程，没评估别开工；"上了线却不知好坏"比没上线更糟（撤不下来、浪费维护费）。②**评估四桶**：domain-specific capability（领域能力）、generation capability（生成能力，含事实一致性+安全）、instruction-following capability（指令遵循，含结构化输出+roleplay）、cost and latency（成本延迟）。**事实一致性三大武器**：local factuality（用 NLI / DeBERTa-v3-base-mnli-fever-anli 等 entailment 分类器判 context 支持）、global factuality（SelfCheckGPT 多次采样自检 / SAFE 用 Google Search 拆句验证 / TruthfulQA 817 题覆盖 38 类），生产中 NLI 分类器最快最便宜。**安全六类**：不当语言、有害建议、仇恨、暴力、刻板、政治/宗教偏见——能用 GPT/Claude/Gemini 当 AI 判官，也能用专门的 Perspective API / Facebook hate speech 模型。**MCQ 不是万能**：能用就用（75% lm-evaluation-harness 任务），但"判别好坏"≠"生成好坏"——MCQ 测的是知识与推理，对生成/翻译/摘要无能为力。**指令遵循**：IFEval（25 类可自动校验指令：关键词/长度/JSON 格式）和 INFOBench（含内容/语言/风格约束，需 yes/no 判官）提供脚手架，但建议自建 benchmark 覆盖你真实业务指令。**Model Selection 四步法**：硬属性（license/数据/大小/隐私）过滤 → 公公开 benchmark 排序 → 自家 pipeline 实跑 → 生产监控+反馈循环。**Build vs Buy** 是个会反复问的问题——API 便宜但有数据外送风险，自托管贵但可控，二者并非二选一（API on top of open source 是新中间态）。**Eval Pipeline 三步**：(1) 评估每个组件（RAG 的 retriever 单独评、Factual consistency 单独评）；(2) 写评估指南（什么算"好"）；(3) 定义评估方法与数据。**关键提醒**：评估指标必须映射到监控指标（生产指标 = 评估指标的子集），否则就是"开发环境打 100 分，生产环境打 0 分"。