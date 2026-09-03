# 《深入理解 AI Agent：设计原理与工程实践》标准知识包

> **一句话**：李博杰（Pine AI 首席科学家）从实战营讲稿整理的 AI Agent 工程实践指南，覆盖 Agent 基础、上下文工程、知识库、工具、Coding Agent、评估、后训练、持续进化、多模态、多 Agent 协作十大主题；核心公式贯穿全书 —— `Agent = LLM + 上下文 + 工具`。

## 书籍元数据

| 字段 | 值 |
|---|---|
| 书名 | 深入理解 AI Agent：设计原理与工程实践 |
| 作者 | 李博杰（@bojieli，Pine AI 首席科学家） |
| 语言 | zh-CN |
| 出版/更新 | 2026-08-10 |
| 标识 | [github.com/bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book) |
| 章节数 | 12（10 章正文 + 引言 + 后记） |
| 字数 | 约 16 万字（12 章 fulltext 总计 980KB） |
| 配套代码 | [github.com/bojieli/ai-agent-book](https://github.com/bojieli/ai-agent-book)（chapter1 ~ chapter10） |

## 覆盖率与数据来源声明（必读）

本知识包源数据为本地 EPUB，按规则四（epub-distill）提取：

| 层 | 完整度 | 来源 |
|---|---|---|
| 章节目录 | ✅ 100% | `EPUB/toc.ncx`（12 个 level-1 节点，每章一个） |
| 原书正文 | ✅ 100% | `EPUB/text/ch001..ch012.xhtml` 全量抓取 → `00-原书档案/fulltext/*.md` |
| 元数据 | ✅ 100% | `EPUB/content.opf`（标题/作者/日期/语言/标识） |
| 提取校验 | sha256 三处一致 | fulltext 文件 / 卡片引用块 / 速查表锚点 |

**编码验证**：OPF/NCX 声明 UTF-8，字节流实测为真实 UTF-8（label "引言" = e5 bc 95 e8 a8 80）；不存在半覆盖。后续如有 weread API 数据混入，需在本文件另行声明。

**三级标记约定**（全包统一）：
- 📖 **原文** = EPUB 全文逐字引用 + 章节定位 `§N.M` + uid 锚点 `chNNN`
- 🧭 **归纳** = 从原文提炼的结构化规则（不引入书中未明说的概念）
- ➕ **补充** = 编者依据公开常识或工程经验补充（非书中内容）

## ⚠️ 引用验证状态（必读）

本知识包 90 张问答卡中，**78 张的 📖原文块通过严格 verbatim 匹配验证**（即 30 字符窗口能在 `00-原书档案/fulltext/chNNN.md` 中找到）。其余 12 张本就只有 🧭归纳 / ➕补充 而无 📖原文块（如 Q3-6/Q5-9/Q6-3/Q7-7/Q8-2/Q8-7/Q9-2/Q9-3/Q9-4/Q10-4/Q10-5 + Q3-11 引用过短）。**有📖块的卡片 verbatim 验证通过率 78/79 = 98%**。

**核验方法**：每张卡的 `章节: ch00X §N.M` 标注可直接定位到 `00-原书档案/fulltext/chNNN.md` 的对应小节。建议对关键卡片做"自己读过才算数"的二次验证——这是知识包读者的责任。

## 目录结构与检索指南

```
AI Agents in Depth/
├── INDEX.md                  ← 本文件：导航入口
├── 00-引言与后记/README.md     导航（非问答）
├── 00-原书档案/              ← 机器可读原始数据
│   ├── book-meta.json           元信息（标题/作者/编码/提取方法）
│   ├── toc.md                   12 章目录（NCX 标题 + 提取标题 + sha256 + 字节数）
│   ├── toc.json                 同上，结构化 JSON
│   └── fulltext/                12 章原文 markdown（按 NCX level-1 切粒）
│       ├── ch001.md  引言
│       ├── ch002.md  第一章 AI Agent 入门
│       ├── ch003.md  第二章 上下文工程
│       ├── ch004.md  第三章 用户记忆和知识库
│       ├── ch005.md  第四章 工具
│       ├── ch006.md  第五章 Coding Agent 与通用 Agent
│       ├── ch007.md  第六章 Agent 的评估
│       ├── ch008.md  第七章 模型后训练
│       ├── ch009.md  第八章 Agent 的持续进化
│       ├── ch010.md  第九章 多模态与实时交互
│       ├── ch011.md  第十章 多 Agent 协作
│       └── ch012.md  后记
├── 01-AI-Agent入门/README.md   Q1-1 ~ Q1-8  第一章核心问答
├── 02-上下文工程/README.md     Q2-1 ~ Q2-13 第二章核心问答
├── 03-用户记忆和知识库/README.md Q3-1 ~ Q3-14
├── 04-工具/README.md           Q4-1 ~ Q4-13
├── 05-Coding-Agent与通用Agent/README.md Q5-1 ~ Q5-9
├── 06-Agent的评估/README.md    Q6-1 ~ Q6-8
├── 07-模型后训练/README.md     Q7-1 ~ Q7-8
├── 08-Agent的持续进化/README.md Q8-1 ~ Q8-7
├── 09-多模态与实时交互/README.md Q9-1 ~ Q9-4
├── 10-多Agent协作/README.md    Q10-1 ~ Q10-6
├── 99-速查表.md              ← 场景→规则速查 + 关键数字（最常调用入口）
└── additions/                ← 你的新理解/新案例/实践结果追加处
    └── README.md                约定 + 模板
```

**给 AI 的检索建议**：
1. 先查 `99-速查表.md` 定位场景 → 回对应模块 README 读原文证据链
2. 按 Q 编号 grep（如 `Q2-3`）可直接命中模块文件中的问题卡片
3. 需要精确出处时读 `00-原书档案/fulltext/chNNN.md`，定位 `§N.M` 小节
4. 引用规则时注意区分 📖原文 / 🧭归纳 / ➕补充 三种性质

## 十大模块速览

| 模块 | 章节范围 | 主题 | 卡片数 |
|---|---|---|---|
| [零 引言与后记](00-引言与后记/README.md) | ch001 + ch012 | 写作背景 / 核心公式回顾 / 学习路径 / 关键术语约定 | 导航（非问答） |
| [一 AI Agent 入门](01-AI-Agent入门/README.md) | ch002 | 核心公式 `Agent = LLM + 上下文 + 工具`、Harness 工程、ReAct 循环、工作流与自主编排、护栏与安全 | 8 |
| [二 上下文工程](02-上下文工程/README.md) | ch003 | **全书最关键章**：API 消息结构、KV Cache 友好设计、提示工程、Agent Skills 按需加载、状态栏、压缩策略 | 13 |
| [三 用户记忆和知识库](03-用户记忆和知识库/README.md) | ch004 | 四种记忆存储格式、三层次评估、RAG 完整栈、稠密+稀疏混合检索、结构化索引、智能体化 RAG | 14 |
| [四 工具](04-工具/README.md) | ch005 | MCP 标准、五类工具（感知/执行/协作/事件/用户沟通）、工具设计原则、事件驱动异步 Agent、Skill 渐进披露 | 13 |
| [五 Coding Agent 与通用 Agent](05-Coding-Agent与通用Agent/README.md) | ch006 | Coding 是元能力、OpenClaw 案例、Harness 在 Coding 中的实践、Agent 自举（代码创造代码） | 9 |
| [六 Agent 的评估](06-Agent的评估/README.md) | ch007 | Pass@k vs Pass^k、LLM-as-a-Judge、评估环境、AB 测试、仿真环境、评估基础设施 | 8 |
| [七 模型后训练](07-模型后训练/README.md) | ch008 | SFT vs RL 三阶段、奖励设计（结果/过程/标量/向量/生成式）、RLVP、On-Policy Distillation、bad case → 后训练 | 8 |
| [八 Agent 的持续进化](08-Agent的持续进化/README.md) | ch009 | 四种更新载体（知识/指令/程序/参数）、可验证闭环、睡眠学习 | 7 |
| [九 多模态与实时交互](09-多模态与实时交互/README.md) | ch010 | 语音三种范式（级联/Omni/全双工）、Computer Use、机器人 VLA、Sim2Real | 4 |
| [十 多 Agent 协作](10-多Agent协作/README.md) | ch011 | 上下文共享×协作拓扑四象限、四种失败模式、Agent 社会、Agent 经济 | 6 |

**总问答卡片数：90 张**（不含 00 模块的导航段落）。每张卡 `## Q编号 题目` + `章节定位` + `📖原文` + `🧭归纳` + `➕补充`（视情况）。

> 新增理解请写入 `additions/`，命名建议：`YYYY-MM-DD-主题.md`
