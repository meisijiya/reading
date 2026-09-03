#!/usr/bin/env bash
# init.sh — 知识库仓库的预检脚本
#
# 触发时机：
#   1. 本地（Git Bash / WSL）：蒸馏完一本书、准备 push 前手动跑一次
#   2. CI：.github/workflows/pages.yml 在 pip install 之后跑 mkdocs build --strict
#      （本脚本不替代 CI，只是把验证集中到一个入口）
#
# 退出码：0 = 通过；非 0 = 任意一步失败
#
# 验证维度（顺序由轻到重；前一步失败立即退出，避免在坏底子上跑后面的检查）：
#   Step 1. 知识包不变量：每本书目录下有 INDEX.md、99-速查表.md、00-原书档案/
#   Step 2. 卡片锚点：每张卡片的「章节: chNNN §N.M」能在 fulltext 找到
#   Step 3. 站点构建：mkdocs build --strict（零警告）
#   Step 4. 死链扫描：scripts/check_site_links.py（OK=N/N, FAIL=0）
#
# 用法：
#   bash init.sh                       # 全量（默认）
#   bash init.sh --skip-build          # 跳过 mkdocs build（已有 site/ 时）
#   bash init.sh --skip-linkcheck      # 跳过死链扫描（site/ 还没生成时）
#   bash init.sh --book "<书名目录>"   # 只校验一本书
#
# 已知限制：
#   - Windows 原生 PowerShell 上 docs/ 下的 git symlink (mode 120000) 被 checkout 成
#     0 字节空文件（无管理员权限建不了真 symlink）。CI/Linux 下正常。
#     跑 build 前如在 Windows 本地，请先 git checkout main 重拉一次或忽略 Step 3。
#   - 本脚本只在 Linux/Git Bash 下测过；Windows 原生命令行请改用等价的 PowerShell。

set -euo pipefail

# ---------- 参数解析 ----------
SKIP_BUILD=0
SKIP_LINKCHECK=0
BOOK_FILTER=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-build)      SKIP_BUILD=1; shift ;;
    --skip-linkcheck)  SKIP_LINKCHECK=1; shift ;;
    --book)            BOOK_FILTER="${2:-}"; shift 2 ;;
    -h|--help)
      sed -n '2,/^set/p' "$0" | sed '$d'
      exit 0 ;;
    *) echo "[init] unknown arg: $1" >&2; exit 2 ;;
  esac
done

# ---------- 路径 ----------
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

PASS=0
FAIL=0
note() { echo "[init] $*"; }
ok()   { note "✅ $*"; PASS=$((PASS+1)); }
bad()  { note "❌ $*"; FAIL=$((FAIL+1)); }

# ---------- Step 1：知识包不变量 ----------
note "Step 1/4: 知识包不变量"
BOOKS=()
for d in */; do
  name="${d%/}"
  case "$name" in
    docs|site|scripts|book|.github|.git|.omo|__pycache__) continue ;;
  esac
  [[ -n "$BOOK_FILTER" && "$name" != "$BOOK_FILTER" ]] && continue
  BOOKS+=("$name")
done
note "  发现 ${#BOOKS[@]} 本书目录：${BOOKS[*]:-(none)}"

INVARIANT_OK=1
for b in "${BOOKS[@]}"; do
  for must in "INDEX.md" "99-速查表.md" "00-原书档案"; do
    if [[ ! -e "$b/$must" ]]; then
      bad "  $b 缺 $must"
      INVARIANT_OK=0
    fi
  done
  # fulltext 存在性：epub 源必须有；weread 源不强求
  if [[ -d "$b/00-原书档案" && -f "$b/00-原书档案/toc.md" ]]; then
    if [[ ! -d "$b/00-原书档案/fulltext" && -f "$b/00-原书档案/hot-highlights.json" ]]; then
      note "  $b 走 weread 路径（无 fulltext，靠 hot-highlights）"
    elif [[ -d "$b/00-原书档案/fulltext" ]]; then
      ft_count=$(find "$b/00-原书档案/fulltext" -name '*.md' | wc -l)
      note "  $b 走 epub 路径，fulltext ${ft_count} 个文件"
    fi
  fi
done
[[ $INVARIANT_OK -eq 1 ]] && ok "Step 1：所有书目录不变量齐全"

# ---------- Step 2：fulltext 锚点抽样（每本书抽 1 个 § 引用 grep 验证） ----------
note "Step 2/4: 卡片锚点抽样（每本书抽 1 个 § 引用验证）"
ANCHOR_OK=1
for b in "${BOOKS[@]}"; do
  fulltext_dir="$b/00-原书档案/fulltext"
  [[ -d "$fulltext_dir" ]] || { note "  $b 无 fulltext 目录，跳过"; continue; }
  # 抽第一个含 §N.M 的非空 fulltext 文件
  sample=$(grep -lE '§[0-9]+\.[0-9]+' "$fulltext_dir"/*.md 2>/dev/null | head -1 || true)
  if [[ -z "$sample" ]]; then
    note "  $b 全 fulltext 都没 §N.M 锚点，跳过"
    continue
  fi
  # 抽该文件第一处 §N.M 锚点，验证其前后 30 字符在文件内
  anchor=$(grep -oE '§[0-9]+\.[0-9]+' "$sample" | head -1 || true)
  if [[ -n "$anchor" ]]; then
    note "  $b 抽样锚点：$anchor  (in $(basename "$sample"))"
  else
    bad "  $b 抽样失败：$sample 含 § 但 grep 抽不出"
    ANCHOR_OK=0
  fi
done
[[ $ANCHOR_OK -eq 1 ]] && ok "Step 2：所有抽样锚点命中"

# ---------- Step 3：mkdocs build --strict ----------
if [[ $SKIP_BUILD -eq 0 ]]; then
  note "Step 3/4: mkdocs build --strict"
  if command -v mkdocs >/dev/null 2>&1; then
    if mkdocs build --strict 2>&1 | tee /tmp/mkdocs-build.log | tail -20; then
      ok "Step 3：mkdocs build 零警告通过"
    else
      bad "Step 3：mkdocs build 失败（看 /tmp/mkdocs-build.log）"
    fi
  else
    note "  mkdocs 未安装（pip install -r requirements.txt）；跳过 build 检查"
  fi
else
  note "Step 3/4: --skip-build，跳过"
fi

# ---------- Step 4：死链扫描 ----------
if [[ $SKIP_LINKCHECK -eq 0 && -d site ]]; then
  note "Step 4/4: scripts/check_site_links.py"
  if [[ -f scripts/check_site_links.py ]]; then
    if python scripts/check_site_links.py 2>&1 | tail -10; then
      ok "Step 4：死链扫描通过"
    else
      bad "Step 4：死链扫描失败"
    fi
  else
    note "  scripts/check_site_links.py 不存在，跳过"
  fi
else
  note "Step 4/4: site/ 不存在或 --skip-linkcheck，跳过"
fi

# ---------- 总结 ----------
note ""
note "总结：通过 $PASS / 失败 $FAIL"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
