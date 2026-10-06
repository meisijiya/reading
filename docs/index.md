# 读书知识库

> 把每一本认真读过的书，蒸馏成可检索、可复用、可演进的标准知识包。

## 阅读建议

!!! tip "怎么用这个知识库"

    1. **遇到具体问题**：先翻每本书的 [`99-速查表.md`](./智能体AI漫游指南（从基础到系统）/99-速查表.md) 定位场景，再跳到对应模块读原文证据链。
    2. **想了解一本书在讲什么**：从该书的 `INDEX.md` 进入，看「模块速览」表格就能掌握全貌。
    3. **需要可引用出处**：进 `00-原书档案/fulltext/`，每张卡的 `📖 原文` 都能在对应 `chNN.md` 里逐字命中。
    4. **想补充自己的理解**：写入对应书目录下的 `additions/`，命名 `YYYY-MM-DD-主题.md`，与速查表同优先级。

证据标记三档：**📖 原文** = 源文件逐字引用 ｜ **🧭 归纳** = 从原文提炼 ｜ **➕ 补充** = 编者依据公开常识补充。

## 已收录

<div class="grid cards" markdown>

- :material-robot:{ .lg .middle } **《智能体 AI 漫游指南：从基础到系统》**

    ---

    Haggai Roitman · v1.3 · 2026

    599 页 / 30 章 6 部分，从 Transformer 基础一路写到多 Agent 系统与 Agentic UI。PPO/DPO/GRPO 逐一推到公式，RAG、记忆、Harness、循环工程、MCP、A2A、框架选型全覆盖。

    :material-bookmark-multiple: **模块数**: 7
    :material-format-list-numbered: **问题数**: 280
    :material-thermometer: **覆盖率**: 100% PDF 全文 · 1672 条原文引用

    [进入 INDEX](./智能体AI漫游指南（从基础到系统）/INDEX.md){ .md-button }
    [速查表](./智能体AI漫游指南（从基础到系统）/99-速查表.md){ .md-button }
    [从基础开始](./智能体AI漫游指南（从基础到系统）/01-基础/README.md){ .md-button }

- :material-brain:{ .lg .middle } **《深入理解 AI Agent：设计原理与工程实践》**

    ---

    李博杰（Pine AI 首席科学家）· 2026-08

    12 章围绕核心公式 `Agent = LLM + 上下文 + 工具` 展开。上下文工程一章最关键——KV Cache 友好设计、Agent Skills 渐进披露、状态栏、压缩策略；另含记忆、工具、Coding Agent、评估、后训练与持续进化。

    :material-bookmark-multiple: **模块数**: 11
    :material-format-list-numbered: **问题数**: 140
    :material-thermometer: **覆盖率**: 100% EPUB 全文 · 920 条原文引用

    [进入 INDEX](./AI%20Agents%20in%20Depth/INDEX.md){ .md-button }
    [速查表](./AI%20Agents%20in%20Depth/99-速查表.md){ .md-button }
    [上下文工程](./AI%20Agents%20in%20Depth/02-上下文工程/README.md){ .md-button }

- :material-scale-balance:{ .lg .middle } **《轻松破解生活难题：民法典100问》**

    ---

    典叔 · 微信读书 89.7 分 · 2024-07 出版

    7 大编 / 100 个高频法律问题，涵盖总则、物权、合同、人格权、婚姻家庭、继承、侵权责任。从胎儿利益到高空抛物，从彩礼到遗嘱，普通人一辈子可能踩的法律坑全覆盖。

    :material-bookmark-multiple: **模块数**: 7
    :material-format-list-numbered: **问题数**: 100

    [进入 INDEX](./民法典100问/INDEX.md){ .md-button }
    [速查表](./民法典100问/99-速查表.md){ .md-button }

- :material-code-braces:{ .lg .middle } **《Claude Code橙皮书：AI编程实战》**

    ---

    花叔 · 本地 epub 一次性落档 · 2025-2026 时效内容

    4 大部分 / 14 个核心章节，从 Claude Code 的独特价值定位、10 分钟起步安装，到 CLAUDE.md / Skill / Hook / MCP 扩展机制与多智能体协作，再到 Chrome 扩展、内容创作自动化、App Store 上架三个完整产品实战。

    :material-bookmark-multiple: **模块数**: 4
    :material-format-list-numbered: **章节数**: 14

    [进入 INDEX](./Claude%20Code橙皮书：AI编程实战%20(花叔)/INDEX.md){ .md-button }
    [速查表](./Claude%20Code橙皮书：AI编程实战%20(花叔)/99-速查表.md){ .md-button }

- :material-lightbulb:{ .lg .middle } **《Vibe Coding：AI 编程时代的认知重构》**

    ---

    张昕东 · 微信读书 71.3 分 · 2025-11 出版

    3 大部分 / 14 个核心问题，从 Karpathy 造词的源起到 Spec/Vibe 双模式实践、上下文工程方法论、「70% 问题」与 Agentic DevOps 前沿，回答「AI 时代程序员还剩什么价值」。

    :material-bookmark-multiple: **模块数**: 3
    :material-format-list-numbered: **问题数**: 14

    [进入 INDEX](./Vibe%20Coding：AI%20编程时代的认知重构/INDEX.md){ .md-button }
    [速查表](./Vibe%20Coding：AI%20编程时代的认知重构/99-速查表.md){ .md-button }

- :material-cloud-outline:{ .lg .middle } **其余 5 本**

    ---

    凤凰架构 · 微服务设计（第2版） · 解构领域驱动设计 · AI Prompt Engineering: The 2026 Guide · AI Engineering (Chip Huyen, 蒸馏中）

    :material-bookmark-multiple: 从分布式演进到领域建模，从云原生架构到 AI 工程方法论

    [凤凰架构](./凤凰架构：构建可靠的大型分布式系统/INDEX.md){ .md-button }
    [微服务设计](./微服务设计（第2版）/INDEX.md){ .md-button }
    [解构 DDD](./解构领域驱动设计/INDEX.md){ .md-button }

</div>

## 知识包结构

每本书都是同一套模板，方便横向迁移和工具识别：

```text
<书名>/
├── INDEX.md              导航入口：元数据 + 覆盖率声明 + 模块速览
├── 00-原书档案/           机器可读原始数据（book-meta.json / toc / fulltext）
├── NN-<模块名>/README.md  每模块一文件，问题卡片化（## Q编号 + 📖原文 + 🧭归纳）
├── 99-速查表.md          场景→规则速查 + 关键数字（最高频调用入口）
└── additions/            增量区：新理解、新案例、实践结果（不改原文档案）
```

!!! note "为什么用 `additions/` 而不是改原文"

    知识包的稳定性来自「原文档案只读 + 增量追加」。你今天顿悟的一条规则，应该写在 `additions/2026-10-06-xxx.md` 里，标注「影响速查表第 X 条」即可覆盖旧条目。原书档案保持冻结，方便未来回溯「这条认知是何时加进来的」。

## 数据来源与覆盖度

!!! info "两本书的源数据不同，覆盖方式也不同"

    | 来源 | 书 | 覆盖方式 |
    |---|---|---|
    | **本地 EPUB** | 深入理解 AI Agent、凤凰架构、微服务设计、解构 DDD 等 | 按 NCX 一级目录逐章抽取，**全文 100%** |
    | **本地 PDF** | 智能体 AI 漫游指南 | 按 PDF 书签 level-2 抽文本层，**全文 100%**（公式排版可能丢失，需对照原书） |
    | **微信读书 API** | 民法典100问、Vibe Coding、Claude Code橙皮书 | API 不提供正文全文，稳定拿到章节目录与热门划线，非热门段落不在公开接口范围内 |

每本书的 `INDEX.md` 顶部都有各自的**覆盖率声明**，写明数据来源与已知局限。

## 校验与维护

!!! example "知识包的质量是怎么保证的"

    ```bash
    # 逐卡验证：每个 📖 引用是否能在 fulltext 里逐字命中
    python scripts/verify_package.py "docs/AI Agents in Depth" "docs/智能体AI漫游指南（从基础到系统）"

    # 站点门禁：零警告才允许 push
    python -m mkdocs build --strict
    python scripts/check_site_links.py
    ```

    验证器**只去空白、不做 NFKC 归一化**——因为 NFKC 会把 `（Pooling）` 压成 `(Pooling)`、`“”` 压成 `""`，把真实的转写错误自动抹平。

## 维护者

站点由 [meisijiya](https://github.com/meisijiya) 维护。每一本书的覆盖率声明与已知局限都写在各自书的 `INDEX.md` 顶部，欢迎按相同规范追加新书。