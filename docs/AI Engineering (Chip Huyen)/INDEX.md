# 《AI Engineering》标准知识包

> **一句话**：Chip Huyen 的 AI 工程方法体系——以"在现成 foundation model 之上构建应用"为命题，串起需求判断 → 模型理解 → 评估方法论 → Prompt/上下文工程 → RAG 与 Agent → 微调 → 数据工程 → 推理优化 → 生产架构 + 用户反馈的完整流水线，强调"系统性优于玄学、评估驱动优于直觉调参"。

## 书籍元数据

| 字段 | 值 |
|---|---|
| 标题 | AI Engineering — Building Applications with Foundation Models |
| 作者 | Chip Huyen（O'Reilly，2024） |
| identifier | `urn:uuid:6e178829-d793-c76f-5b38-f1db8b86265e`（按 sha256 前缀缩位，仅作内部标识） |
| 语言 | `en` |
| 出版社 | O'Reilly Media, Inc. |
| 出版日期 | 2024（Copyright 2025 Developer Experience Advisory LLC，ISBN 978-1-098-16630-4） |
| fileSha256 | `6e178829d793c76f5b38f1db8b86265e1054c6779aa6a16505fb7aab36d35458` |
| fileSize | 30,752,448 字节（约 29.3 MB） |
| fulltextCount | 12 个 fulltext 文件（1 前言 + 10 章正文 + 1 尾声） |
| 打开源文件 | `book/AI Engineering (Chip Huyen) (z-library.sk, 1lib.sk, z-lib.sk).epub`（本地 epub，未发布到 GitHub Pages） |

> 元数据来源：[`00-原书档案/book-meta.json`](00-原书档案/book-meta.json)（与原书 OPF 一致）；完整章节表见 [`00-原书档案/toc.md`](00-原书档案/toc.md)。

## 覆盖率与数据来源声明

本知识包通过 **epub 一次性落档** 构建——`ebooklib` + `BeautifulSoup` 解析原书 OPF/NCX → 12 个 fulltext 文件（1 前言 + 第 1-10 章 + 1 尾声）完整正文落盘 `fulltext/`，提炼层只从原文归纳，禁止凭模型常识编造「书中观点」。

| 层 | 完整度 | 来源 |
|---|---|---|
| 章节目录（1 前言 + 10 章 + 1 尾声） | ✅ 100% | epub 解析（[`toc.md`](00-原书档案/toc.md)） |
| 原书文本（12 篇正文 + 全部小节） | ✅ 100% | epub fulltext（`fulltext/uid-NN-*.md`，约 174K 词） |
| 方法提炼（每章卡片 + 速查表） | 由上述原文归纳 + 编者补充公开常识 | 见下方三级标记约定 |

**未纳入 fulltext 的部分**（NCX 顶层节点但非「Chapter N」粒度）：Index、About the Author、Colophon。这些是出版元信息与索引页，与方法论正文无关。

**证据标记约定**（全包统一，**无热度括号**——epub 无 heat 概念）：

- 📖 **原文** = epub fulltext 逐字引用，未改动；附 `§N.M`（章节内小节）+ `uid NN`（fulltext 文件编号）双锚点
- 🧭 **归纳** = 编者从原文提炼的结构化结论
- ➕ **补充** = 编者依据公开常识补充（非原书内容）

## 目录结构与检索指南

```
AI Engineering (Chip Huyen)/
├── INDEX.md                    ← 本文件：导航入口
├── 00-原书档案/                  ← 原始数据（机器可读）
│   ├── book-meta.json              书籍元信息（OPF 提取）
│   ├── toc.md                      12 个 fulltext 的目录表
│   ├── epub/                       原书 epub 归档
│   └── fulltext/                   ← 12 个完整正文（uid-NN-题名.md）
├── 01-基础与理解/README.md      前言 + §1 AI 工程起源 + §2 理解 Foundation Model
├── 02-评估方法/README.md        §3 评估方法论 + §4 评估 AI 系统
├── 03-Prompt与上下文/README.md  §5 Prompt 工程 + §6 RAG 与 Agent
├── 04-微调与数据/README.md      §7 微调 + §8 数据工程
├── 05-推理优化与架构/README.md  §9 推理优化 + §10 架构与用户反馈
├── 06-尾声/README.md            尾声：AI 工程的开放问题
├── 99-速查表.md                  ← 场景→规则速查 + AI 工程关键数字（最常调用入口）
└── additions/                  ← 你的新理解/新案例/实践结果追加处
    └── README.md
```

## 六大模块速览

| 模块 | 章节 | 主题 |
|---|---|---|
| [一 基础与理解](01-基础与理解/README.md) | 前言 + §1-§2（3 篇） | AI 工程学科三成因（scale 模型 + model-as-a-service + 低准入门槛）→ 8 大应用分类 → Foundation Model 训练数据/架构/规模/后训练/采样 → Chinchilla 缩放律 → Transformer + Mamba/Jamba 替代架构 → Probabilistic Nature of AI |
| [二 评估方法](02-评估方法/README.md) | §3-§4（2 章） | LM 度量四件套（entropy / cross entropy / BPC / BPB / perplexity）→ 精确评估（functional correctness + similarity + embedding）→ AI as a judge → Comparative eval（Chatbot Arena Elo）→ 评估四桶（领域能力 / 生成 / 指令遵循 / 成本延迟）→ Model Selection 四步法 |
| [三 Prompt 与上下文](03-Prompt与上下文/README.md) | §5-§6（2 章） | In-context learning（zero/few-shot）+ system vs user prompt + context efficiency → 7 大最佳实践（clear/context/decompose/time-to-think/iterate/tools/version）→ 3 大防御性攻击（prompt 提取 / jailbreak / 信息提取）→ RAG 架构（term-based BM25 + embedding-based + hybrid）→ RAG 优化（chunking/reranking/query rewriting/contextual）→ Agent（tools/planning/failure modes） |
| [四 微调与数据](04-微调与数据/README.md) | §7-§8（2 章） | Finetuning 三种取舍（理由/不理由/RAG 关系）→ 内存四件套（weights + activations + gradients + optimizer states）→ 数值格式（FP32/FP16/BF16/INT8/INT4/1-bit）→ 量化（PTQ / QLoRA）→ PEFT → 模型合并 → 数据三黄金（quality/coverage/quantity）→ 数据合成（传统 + AI-powered + distillation）→ 数据处理四步 |
| [五 推理优化与架构](05-推理优化与架构/README.md) | §9-§10（2 章） | 推理两阶段（prefill compute-bound + decode memory-bound）→ 性能度量（TTFT/TPOT/throughput/goodput/MFU/MBU）→ AI 加速器（GPU/TPU/LPU）→ 模型优化（quantization/distillation/pruning/arch search）→ 服务优化（batching/KV cache/prompt cache/speculative decoding）→ 架构五步（context → guardrails → router/gateway → cache → agent）→ 用户反馈系统设计 |
| [六 尾声](06-尾声/README.md) | 尾声 | 150,000 词 / 160 插图 / 250 脚注 / 975 引用；AI 工程的开放问题 |

## 完整章节目录（直链完整原文）

> 章节标题直接链到 `00-原书档案/fulltext/uid-NN-*.md` 完整原文页。每章独立可读，无需经过模块页。

| 章节 | UID | 字数 | 所属 | 原文 |
|---|---|---:|---|---|
| Preface 前言 | 01 | 3,944 | 基础与理解 | [完整原文](00-原书档案/fulltext/uid-01-Preface.md) |
| §1 第1章 Introduction to Building AI Applications with Foundation Models | 02 | 15,736 | 基础与理解 | [完整原文](00-原书档案/fulltext/uid-02-Introduction-to-Building-AI-Applications-with-Foundation-Models.md) |
| §2 第2章 Understanding Foundation Models | 03 | 19,938 | 基础与理解 | [完整原文](00-原书档案/fulltext/uid-03-Understanding-Foundation-Models.md) |
| §3 第3章 Evaluation Methodology | 04 | 15,600 | 评估方法 | [完整原文](00-原书档案/fulltext/uid-04-Evaluation-Methodology.md) |
| §4 第4章 Evaluate AI Systems | 05 | 18,880 | 评估方法 | [完整原文](00-原书档案/fulltext/uid-05-Evaluate-AI-Systems.md) |
| §5 第5章 Prompt Engineering | 06 | 12,527 | Prompt 与上下文 | [完整原文](00-原书档案/fulltext/uid-06-Prompt-Engineering.md) |
| §6 第6章 RAG and Agents | 07 | 17,954 | Prompt 与上下文 | [完整原文](00-原书档案/fulltext/uid-07-RAG-and-Agents.md) |
| §7 第7章 Finetuning | 08 | 18,468 | 微调与数据 | [完整原文](00-原书档案/fulltext/uid-08-Finetuning.md) |
| §8 第8章 Dataset Engineering | 09 | 14,498 | 微调与数据 | [完整原文](00-原书档案/fulltext/uid-09-Dataset-Engineering.md) |
| §9 第9章 Inference Optimization | 10 | 13,649 | 推理优化与架构 | [完整原文](00-原书档案/fulltext/uid-10-Inference-Optimization.md) |
| §10 第10章 AI Engineering Architecture and User Feedback | 11 | 13,219 | 推理优化与架构 | [完整原文](00-原书档案/fulltext/uid-11-AI-Engineering-Architecture-and-User-Feedback.md) |
| Epilogue 尾声 | 12 | 239 | 尾声 | [完整原文](00-原书档案/fulltext/uid-12-Epilogue.md) |

## AI 检索指南

- **查具体规则/结论** → 先查 [`99-速查表.md`](99-速查表.md)，条目带 §N.M 锚点，可回溯到模块卡片的 📖原文引用。
- **查某主题的原文证据** → 上方章节目录点进 `fulltext/uid-NN-*.md` 完整原文页；或到对应 `NN-模块/README.md` 看逐字引用。
- **AI 引用规范**：🧭归纳与➕补充不得冒充原文；引用请带上 `§N.M` 锚点与 uid 编号。
- **增量内容**：`additions/*.md` 与速查表同优先级，标注「影响」的条目覆盖速查表旧条目。

## 阅读建议路径

按本书"应用开发流程"顺序读一遍，再回头读相关章节做深挖：

1. 先读 [§1 概览](01-基础与理解/README.md) → 看 AI 工程的学科轮廓、8 大应用场景
2. 再读 [§2 理解 FM](01-基础与理解/README.md) → 补 Transformer / sampling / scaling law 等下层概念
3. 然后进 [§3-§4 评估](02-评估方法/README.md) → 评估驱动开发是全书的隐线，**没评估别往下走**
4. [§5 Prompt](03-Prompt与上下文/README.md) → 第一波成本最低的优化
5. [§6 RAG + Agent](03-Prompt与上下文/README.md) → 信息缺失型失败的解药
6. [§7 微调](04-微调与数据/README.md) → 行为/格式型失败的解药（成本陡升）
7. [§8 数据](04-微调与数据/README.md) → 数据质量决定一切
8. [§9 推理优化](05-推理优化与架构/README.md) → 成本与延迟优化
9. [§10 架构与反馈](05-推理优化与架构/README.md) → 端到端系统设计与数据飞轮
10. 任意阶段用 [99-速查表](99-速查表.md) 做日常 cheat-sheet