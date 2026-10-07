# 四 微调与数据（§7-§8）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

## §7 第7章 Finetuning

- **章节 UID**: 08
- **章节号**: §7
- **字数**: 18,468
- **父模块**: 微调与数据
- **原文出处**: [`uid-08-Finetuning.md`](../00-原书档案/fulltext/uid-08-Finetuning.md)

> 📖 **原文**（§7.0）：Finetuning is the process of adapting a model to a specific task by further training the whole model or part of the model. Chapters 5 and 6 discuss prompt-based methods, which adapt a model by giving it instructions, context, and tools. Finetuning adapts a model by adjusting its weights.

> 📖 **原文**（§7.0）：Compared to prompt-based methods, finetuning incurs a much higher memory footprint. At the scale of today's foundation models, naive finetuning often requires more memory than what's available on a single GPU. This makes finetuning expensive and challenging to do.

> 📖 **原文**（§7.1 Finetuning 类型）：Recall that a model's training process starts with *pre-training*, which is usually done with self-supervision. … Before finetuning this pre-trained model with expensive task-specific data, you can finetune it with self-supervision using cheap task-related data. *Self-supervised finetuning* is also called *continued pre-training*.

> 📖 **原文**（§7.1）：A model can also be finetuned with reinforcement learning to generate responses that maximize human preference. Preference finetuning requires comparative data that typically follows the format (instruction, winning response, losing response). … It's possible to finetune a model to extend its context length. *Long-context finetuning* typically requires modifying the model's architecture.

> 📖 **原文**（§7.2 何时微调）：The primary reason for finetuning is to improve a model's quality, in terms of both general capabilities and task-specific capabilities. Finetuning is commonly used to improve a model's ability to generate outputs following specific structures, such as JSON or YAML formats.

> 📖 **原文**（§7.2 何时不微调）：While finetuning can improve a model in many ways, many of these improvements can also be achieved, to a certain extent, without finetuning. … First, while finetuning a model for a specific task can improve its performance for that task, it can degrade its performance for other tasks.

> 📖 **原文**（§7.2）：AI engineering experiments should start with prompting, following the best practices. Explore more advanced solutions only if prompting alone proves inadequate. … In the vast majority of cases, you should see improvements after finetuning with 50–100 examples.

> 📖 **原文**（§7.3 RAG vs 微调）：*If the model fails because it lacks information, a RAG system that gives the model access to the relevant sources of information can help*. Information-based failures happen when the outputs are factually wrong or outdated. … *In short, finetuning is for form, and RAG is for facts*.

> 📖 **原文**（§7.3）：RAG can also introduce a more significant performance boost than finetuning. Ovadia et al. (2024) showed that for almost all question categories in the MMLU benchmark, RAG outperforms finetuning for three different models: Mistral 7B, Llama 2-7B, and Orca 2-7B.

> 📖 **原文**（§7.4 内存）：During the backward pass, each trainable parameter comes with additional values, its gradient, and its optimizer states. Therefore, the more trainable parameters there are, the more memory is needed to store these additional values.

> 📖 **原文**（§7.4 内存公式）：Inference memory = N × M × 1.2 (where N = params, M = bytes per param; the 1.2 accounts for activations + KV cache). Training memory = weights + activations + gradients + optimizer states.

> 📖 **原文**（§7.5 数值格式）：FP32 uses 32 bits (4 bytes) to represent a float. … FP16 uses 16 bits (2 bytes) and is called half precision. … Other popular floating point formats in AI workloads include BF16 (BFloat16) and TF32 (TensorFloat-32). BF16 was designed by Google to optimize AI performance on TPUs.

> 📖 **原文**（§7.5 BF16 vs FP16）：Even though BF16 and FP16 have the same number of bits, BF16 has more bits for range and fewer bits for precision. This allows BF16 to represent large values that are out-of-bound for FP16. However, this also makes BF16 less precise than FP16.

> 📖 **原文**（§7.5 量化）：The fewer bits needed to represent a model's values, the lower the model's memory footprint will be. A 10B-parameter model in a 32-bit format requires 40 GB for its weights, but the same model in a 16-bit format will require only 20 GB. Reducing precision, also known as quantization, is a cheap and extremely effective way to reduce a model's memory footprint.

> 📖 **原文**（§7.6 PEFT）：A memory-efficient approach that has become dominant in the finetuning space is PEFT (parameter-efficient finetuning). PEFT methods only update a small number of parameters while keeping the rest frozen, dramatically reducing the memory required for training.

> 📖 **原文**（§7.6 LoRA）：LoRA (Low-Rank Adaptation) injects trainable low-rank decomposition matrices into each transformer layer. … The original weights are frozen, and only the low-rank matrices are trained. This reduces the number of trainable parameters by orders of magnitude.

> 📖 **原文**（§7.7 模型合并）：Model merging combines the weights of multiple finetuned models into a single model, often producing a model that combines the strengths of all merged models. Common merging techniques include linear averaging, SLERP (Spherical Linear Interpolation), and task arithmetic.

> 🧭 **归纳**：Finetuning 是三板斧（Prompt/RAG/Finetuning）中最重的一种——能改权重但成本陡升。**先做 Prompt → 加 RAG → 还不行再微调**——这是本书反复强调的次序；50-100 例微调通常就能看到明显改进，但若小数据下无效，大数据也基本无效。**Finetuning 三类**：① continued pre-training（自监督，加领域语料继续预训练）；② supervised finetuning / SFT（指令-响应对）；③ preference finetuning / RLHF（指令-胜出响应-失败响应三元组）。**Finetuning vs RAG**——一句话："**Finetuning is for form, RAG is for facts**"。信息缺失/过时/事实错误 → RAG；输出格式不对/行为不符预期/不循指令 → 微调；两者非互斥，可叠加（Ovadia 2024 显示 43% 情况下 RAG+微调 > 单 RAG）。**Finetuning 不做的理由**：(a) 任务型微调会损伤其他任务能力（catastrophic forgetting）；(b) 高质量标注数据贵且慢；(c) 需要训练 ML 知识（学习率、optimizer、loss 监控）；(d) 需要维护基础设施（自托管推理）；(e) 数据飞轮可能跑得比微调更快。**内存四大件** = 权重 + 激活 + 梯度 + 优化器状态；用 Adam 时每个 trainable param 多 3 个 value（gradient + 2 个 optimizer state）——所以减少 trainable params 是 PEFT 的根。**数值格式铁三角**：FP32（4B/param）= 训练默认；FP16（2B/param）= 推理常用；BF16（2B/param，range 更宽精度更窄，TPU 优化）= 大模型推理必选；INT8/INT4 = 量化版，省 50-87.5% 显存。**量化是减少内存的"最便宜的银弹"**——PTQ（训练后量化）最常见，QLoRA 把基础模型量化到 4-bit + LoRA 微调让消费级 GPU 能跑 65B 模型。**PEFT = parameter-efficient finetuning**：LoRA 用低秩分解冻结原始权重只训小矩阵；QLoRA = 4-bit 量化基础 + LoRA；DoRA / Adapter 等变体。**模型合并**：把多个微调过的模型权重合并（线性平均 / SLERP / task arithmetic），可低成本"取各家之长"，无需额外训练。**1-bit LLM 萌芽**：BitNet b1.58 用 1.58 bit/param，性能比肩 16-bit Llama 2（≤3.9B 参数），代表量化极限。

## §8 第8章 Dataset Engineering

- **章节 UID**: 09
- **章节号**: §8
- **字数**: 14,498
- **父模块**: 微调与数据
- **原文出处**: [`uid-09-Dataset-Engineering.md`](../00-原书档案/fulltext/uid-09-Dataset-Engineering.md)

> 📖 **原文**（§8.0）：The quality of a model depends on the quality of its training data. The best ML team in the world with infinite compute can't help you finetune a good model if you don't have data. The goal of dataset engineering is to create a dataset that allows you to train the best model, ideally within your allocated budget.

> 📖 **原文**（§8.0）：Data operations have evolved from side tasks that people handle when they have time to dedicated roles. Many AI companies now employ data labelers, dataset creators, and data quality engineers, either integrated into or working alongside their core engineering teams.

> 📖 **原文**（§8.0）：Data will mostly just be toil, tears, and sweat.

> 📖 **原文**（§8.0）：Model-centric AI tries to improve AI performance by enhancing the models themselves. … Data-centric AI tries to improve AI performance by enhancing the data.

> 📖 **原文**（§8.1 数据三黄金）：At a high level, data curation follows the three criteria: data quality, data coverage, and data quantity.

> 📖 **原文**（§8.1 Quality）：In general, data can be considered high-quality if it has the following six characteristics: relevant, aligned with task requirements, consistent, correctly formatted, sufficiently unique, and compliant.

> 📖 **原文**（§8.1）：A small amount of high-quality data can outperform a large amount of noisy data, e.g., data that is irrelevant or inconsistent. The creators of the Yi model family found that 10K carefully crafted instructions are superior to hundreds of thousands of noisy instructions.

> 📖 **原文**（§8.1 LIMA）："LIMA: Less Is More for Alignment" shows that a 65B-parameter Llama model, finetuned with 1,000 carefully curated prompts and responses, can produce answers that are either equivalent or strictly preferred to GPT-4 in 43% of cases.

> 📖 **原文**（§8.1 Coverage）：A model's training data should cover the range of problems you expect it to solve. … For general-purpose use cases like chatbots, the finetuning data should be diverse, representing a wide range of topics and speaking patterns.

> 📖 **原文**（§8.1 Quantity）：While millions of examples sounds like a lot, it's small compared to the data typically needed to train a foundation model from scratch. For reference, Llama 2 and Llama 3 were trained using 2 trillion and 16 trillion tokens, respectively.

> 📖 **原文**（§8.1）：You might wonder: if I have millions of examples, shouldn't I just train a model from scratch? You can and should evaluate whether training a model from scratch would improve your performance. … This is due to a phenomenon called *ossification*, where pre-training can *ossify* (i.e., freeze) the model weights so that they don't adapt as well to the finetuning data. Smaller models are more susceptible to ossification than larger models.

> 📖 **原文**（§8.2 数据获取）：The most important source of data, however, is typically data from your own application. If you can figure out a way to create a *data flywheel* that leverages data generated by your users to continually improve your product, you will gain a significant advantage.

> 📖 **原文**（§8.2）：Before investing in creating your own data, check available datasets first. … Always check a dataset's license before using it. Try your best to understand where the data comes from. Even if a dataset has a license that allows commercial use, it's possible that part of it comes from a source that doesn't.

> 📖 **原文**（§8.2 Annotation）：Some teams, including LinkedIn, have reported that annotation guidelines were among the most challenging parts of their AI engineering pipeline. It's alarming how often people abandon careful annotation halfway due to the time and effort required.

> 📖 **原文**（§8.3 数据合成）：The biggest reason for data synthesis is that it allows you to produce data at scale, promising an abundant supply of data for training and testing AI models. … You can also synthesize data to mitigate privacy concerns and distill models.

> 📖 **原文**（§8.3 Model Distillation）：Distillation is a technique where a smaller student model is trained to mimic a larger teacher model. The student learns from the teacher's outputs (logits, probabilities, or generated text), often achieving performance close to the teacher while being much smaller and cheaper to run.

> 📖 **原文**（§8.3 Limitations）：AI-generated data can inherit the biases and blind spots of the model that generated it. If your base model has systematic errors, synthetic data will amplify them rather than correct them. … A common approach is to mix human-generated and AI-generated data, with human data serving as the anchor for quality.

> 📖 **原文**（§8.4 数据处理）：Four steps: Inspect Data (look at examples directly), Deduplicate Data (duplicates cause biases and contamination), Clean and Filter Data (remove low-quality), Format Data (consistent schema, tokenize consistently).

> 🧭 **归纳**：数据决定模型上限；"最好的 ML 团队 + 无限算力，没数据也训不出好模型"。**Data-centric vs Model-centric**：过去十年研究都聚焦"同一个数据集上谁家模型更好"（model-centric），近年转向"同一个模型谁家数据集更好"（data-centric，DataComp/DataPerf 等比赛）。**数据三黄金**——quality / coverage / quantity——烹饪比喻：quality 是食材新鲜度（坏食材做不出好菜），coverage 是配料齐全（不能太多糖也不能没有糖），quantity 是食材份量。**Quality 六特性** = relevant + aligned + consistent + correctly formatted + unique + compliant；Yi 用 10K 精心构造指令 > 数十万噪音指令；LIMA 用 1,000 条精选 prompt-response 训 65B Llama，在 43% 案例上不输 GPT-4。**Coverage 维度多样**：不同说话风格/语言/长度/任务类型——Llama 3 性能提升主要靠"数据质量 + 多样性 + 训练规模"（不是架构创新）。**Quantity 经验法则**：从 50-100 例起步看是否有效；finetuning technique（full vs PEFT）、task complexity、base model performance 决定需要量；性能增益曲线一般快速达到 plateau（边际收益递减）。**数据飞轮 (data flywheel)** = 应用产生用户数据 → 反馈回流到训练 → 模型变好 → 用户更多 → 更多数据——这是大厂的核心壁垒。**公共数据集来源**：Hugging Face / Kaggle / Google Dataset Search / Data.gov / Kaggle competition / TensorFlow datasets / EleutherAI's lm-evaluation-harness。**Annotation Guideline 比想象中难**：LinkedIn 说标注指南是 AI 工程流水线最难的部分；很多人放弃精标，寄希望"模型自己悟"——风险大。**Data Augmentation vs Synthesis**：augmentation 从真实数据衍生（图像翻转），synthesis 从无到有生成。**Model Distillation**（一种合成形式）= 小模型学大模型输出 logits/probabilities/text，可让 7B 模型逼近 65B 模型。**AI 生成数据的隐忧**：继承 base model 的偏见 + 放大系统错误；解决 = 与人类数据混合（人类数据作 quality anchor）。**数据处理四步**：(1) Inspect（人工抽样看）；(2) Deduplicate（去重防偏见+污染）；(3) Clean/Filter（去低质）；(4) Format（统一 schema、用模型 tokenizer 切分）。