# 读书知识库

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/site-mkdocs--material-blue)](https://meisijiya.github.io/reading/)

个人读书笔记的知识库。每本书一个目录，结构化沉淀划线、原文引用、个人归纳与速查表。新书进来 README 不动 —— 一切按 `AGENTS.md` 的蒸馏规约。

## 数据源

- **微信读书接口**（规则二）：书名 → bookId → 章节目录 → 每章热门划线（markText + heat 标记人数）。这是唯一能拿到的原文片段来源。
- **本地 epub**（规则四）：`ebooklib` 解析 NCX level 1 节点，`fulltext/` 即原书全部正文（覆盖度天然 100%）。

## 知识包结构

```
<书名>/
├── INDEX.md              导航入口：元数据 + 覆盖率声明 + 目录树 + AI 检索指南 + 模块速览
├── 00-原书档案/           机器可读原始数据
│   ├── book-meta.json
│   ├── toc.md / toc.json
│   ├── hot-highlights.json        （微信读书来源）
│   └── fulltext/uid-NN-*.md       （epub 来源，一章一文件）
├── NN-<模块名>/README.md  每模块一文件；每问/每章一张卡片
├── 99-速查表.md          场景 → 规则速查 + 关键期限数字
└── additions/            增量区：README.md（约定+模板）+ YYYY-MM-DD-主题.md
```

验收：问题卡片数 == 目录问题数；引用条数 == 抓取条数；additions/ 就位。

## 三级标记

全包统一，互不冒充：

| 标记 | 含义 | 锚点 |
| --- | --- | --- |
| 📖原文 | 接口逐字引用 | 微信读书：含热度人数；epub：含 `§N.M` + `uid NN` 双锚点 |
| 🧭归纳 | 从原文提炼 | — |
| ➕补充 | 编者依据公开常识 | — |

提炼层只能从原文归纳，禁止凭模型常识编造"书中观点"。

## 覆盖率声明

`INDEX.md` 顶部写明各层数据来源与完整度：

- **微信读书来源**：接口拿不到正文章节全文，半覆盖。升级路径 — 用户导出全文放入 `00-原书档案/fulltext/` 即完成归档，其余结构不动。
- **epub 来源**：`fulltext/` 即原书全部正文，覆盖度 100%。

## 增量维护

读者新内容一律追加到 `additions/YYYY-MM-DD-主题.md`（模板见该目录 README），不改原文档案；与既有规则冲突时在 additions 里写明理由，保留演化历史。

AI 检索时 additions 与速查表同优先级，标注了"影响"的条目覆盖速查表对应旧条目。

## 站点发布

`push → meisijiya/reading:main` 自动触发 GitHub Actions 构建并发布到 <https://meisijiya.github.io/reading/>。新增书目录必须同步两处契约 —— `mkdocs.yml` 的 `nav:` 加一行 + `docs/` 下建一个 symlink，详见 `AGENTS.md` 规则三。

## 本地预览

```bash
pip install -r requirements.txt
mkdocs serve
```

打开 <http://127.0.0.1:8000/reading/>。

## License

本仓库采用 [MIT License](LICENSE)。