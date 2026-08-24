# 《Claude Code橙皮书：AI编程实战》标准知识包

> **一句话**：花叔主笔的 Claude Code 中文实战手册——从为什么选它、10分钟起步安装配置，到 CLAUDE.md / Skill / Hook / MCP 扩展与多智能体协作，再到 Chrome 扩展 / 内容创作自动化 / App Store 上架三个完整产品实战，构建 AI 编程时代完整工作流。

## 书籍元数据

| 字段 | 值 |
|---|---|
| 标题 | Claude Code橙皮书：AI编程实战 |
| 作者 | 花叔 |
| identifier | `7577c1d1-e48d-4510-80ff-fa9c0054f92b` |
| 语言 | `zh-CN` |
| fileSha256 | `039ef554dd83c7836261f838067f545f5486e9241c35183ea33c81341b720d05` |
| fileSize | 5,049,246 字节（约 4.8 MB） |
| spineItemsCount | 14 |
| ncxChapterCount | 14 |
| ncxSubchapterCount | 119 |
| partCount | 4 |
| 打开源文件 | `book/Claude Code橙皮书AI编程实战 (花叔) (z-library.sk, 1lib.sk, z-lib.sk).epub`（本地 epub，未发布到 GitHub Pages） |

> 元数据来源：[`00-原书档案/book-meta.json`](00-原书档案/book-meta.json)（与原书 OPF + NCX 一致）。

## 覆盖率与数据来源声明

本知识包通过 **epub 一次性落档** 构建——`ebooklib` 解析原书 OPF/NCX → 14 个章节全部按 NCX level 1 节点拆出完整正文落盘 `fulltext/`，提炼层只从原文归纳，禁止凭模型常识编造「书中观点」。

| 层 | 完整度 | 来源 |
|---|---|---|
| 章节目录（4 部分 × 14 章） | ✅ 100% | epub NCX 解析（[`toc.md`](00-原书档案/toc.md)） |
| 原书文本（14 章正文 + 119 子节） | ✅ 100% | epub fulltext（`fulltext/uid-NN-题名.md`） |
| 方法提炼（每章卡片 + 速查表） | 由上述原文归纳 + 编者补充公开常识 | 见下方三级标记约定 |

**证据标记约定**（全包统一，**无热度括号**——epub 无 heat 概念）：

- 📖 **原文** = epub fulltext 逐字引用，未改动；附 `§N.M` 章节内小节锚点 + `uid NN` fulltext 文件编号
- 🧭 **归纳** = 编者从原文提炼的结构化结论
- ➕ **补充** = 编者依据公开常识补充（非原书内容）

**升级路径**：N/A（本包覆盖率已 100%，无需再升级；若日后原书修订，重新解析 epub 覆盖 `fulltext/` 即可）。

## 目录结构与检索指南

```
Claude Code橙皮书：AI编程实战 (花叔)/
├── INDEX.md                  ← 本文件：导航入口
├── 00-原书档案/               ← 原始数据（机器可读）
│   ├── book-meta.json            书籍元信息（OPF + NCX 提取）
│   ├── toc.md                    14 章目录表（uid|level|chapterNumber|title|wordCount|parentPart）
│   ├── epub/                     原书 epub 归档
│   │   └── Claude Code橙皮书AI编程实战 (花叔) (z-library.sk, 1lib.sk, z-lib.sk).epub
│   ├── fulltext/                 ← 14 章完整正文（uid-NN-题名.md，NCX level 1 一节点一文件）
│   └── assets/                   原书插图资源
├── 01-第一部分/README.md      §1-§3 选择Claude Code / 起步 / 第一个项目
├── 02-第二部分/README.md      §4-§6 核心工作模式 / CLAUDE.md / 进阶对话
├── 03-第三部分/README.md      §7-§11 扩展能力 / 多智能体 / 完整产品 / 避坑 / 心智
├── 04-第四部分/README.md      §12-§14 三个实战项目（Chrome扩展 / 内容创作 / App Store 上架）
├── 99-速查表.md               ← 场景→方法速查 + 关键数字（最常调用入口）
└── additions/                 ← 你的新理解/新案例/实践结果追加处
    └── README.md
```

**给 AI 的检索建议**：

1. **小节级精确定位**：按 `§N.M` 锚点 grep 可直接命中某章某小节——
   ```bash
   grep '§1.1' "Claude Code橙皮书：AI编程实战 (花叔)/01-第一部分/README.md"
   # → 命中 uid=01 章节下 §1.1 小节的全部卡片引用块
   ```
2. **章节定位**：按 `uid` 编号 grep 命中整章卡片集合——
   ```bash
   grep '^uid: 07' "Claude Code橙皮书：AI编程实战 (花叔)/00-原书档案/fulltext/"
   ```
3. **场景速查**：先查 `99-速查表.md` 定位场景/概念 → 再回对应 `NN-第N部分/README.md` 读原文证据链
4. **查 frontmatter 元数据**：每张卡片顶部 frontmatter 含 `uid / level / chapterNumber / title / wordCount / parentPart`，可与 `toc.md` 表头交叉对账
5. **回溯原书**：卡片引用的 `§N.M` 锚点可在 `00-原书档案/fulltext/uid-NN-题名.md` 中找到对应小节 verbatim 原文
6. **引用时严格区分** 📖原文 / 🧭归纳 / ➕补充 三种性质；本包「📖原文」无热度括号（epub 无 heat 字段）
7. 用户增量认知在 `additions/`，与速查表同优先级，标注「影响」的条目覆盖旧条目

## 四大模块速览

| 模块 | 章节 | 主题 |
|---|---|---|
| [一 第一部分](01-第一部分/README.md) | §1-§3（3章） | 入门篇：为什么选 Claude Code（终端 AI 编程 vs IDE 插件）、10 分钟快速起步（安装/账号/首个指令）、第一个项目实战（从零到可运行 demo） |
| [二 第二部分](02-第二部分/README.md) | §4-§6（3章） | 核心篇：把 Claude Code 变成生产力工具的工作模式（交互式/批处理/计划模式）、CLAUDE.md 给 AI 一张项目地图（上下文工程）、进阶对话技巧（提示策略与反馈循环） |
| [三 第三部分](03-第三部分/README.md) | §7-§11（5章） | 进阶篇：扩展能力（Skill / Hook / MCP 协议）、多智能体协作（Subagent / Task 编排）、从零构建完整产品的工程化流程、避坑指南（AI 编程的边界与常见陷阱）、心智模型与持续进化 |
| [四 第四部分](04-第四部分/README.md) | §12-§14（3章） | 实战篇：Chrome 扩展从设计到发布、内容创作自动化流水线（抓取/改写/排版）、完整产品上 App Store 付费榜第一的复盘 |

> 新增理解请写入 `additions/`，命名建议：`YYYY-MM-DD-主题.md`
