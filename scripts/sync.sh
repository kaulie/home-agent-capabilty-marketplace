#!/usr/bin/env bash
#
# 同步能力目录：从 home-agent-os 导出 → **导入 marketplace 数据库** → 从库里导出 catalog。
#
#   scripts/sync.sh /path/to/home-agent-os          # 导出（**声明层**）+ 入库 + 回写 + 自检 + 提交
#   scripts/sync.sh /path/to/home-agent-os --check  # 只对账（CI）：与代码比对，有漂移非零退出
#
# 定位：集市是「能力展示与技能介绍」——只登记**声明**（能力/服务/条件挂载/参数/触发语/文档 + 人工策展），
# 不保存任何实时状态（在线、设备、探测结果）。要看实时状态请用 Brain `GET /api/v1/capabilities`。
#
# 数据流（**库是权威，catalog/capabilities.json 是库的导出**）：
#   home-agent-os 代码 ──导出器──▶ 临时 catalog.json ──导入──▶ SQLite（保留集市注解）
#        └─▶ capabilities/*.md + catalog/capabilities.md（代码视图，随代码 PR 审阅）
#        └─▶ 库导出 ─▶ catalog/capabilities.json（声明视图 + 集市注解，供静态 UI/Pages/diff）
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOS="${1:-}"
shift || true
CHECK=""
for arg in "$@"; do
  case "$arg" in
    --check) CHECK="--check" ;;
    *) echo "[sync][错误] 未知参数 $arg" >&2; exit 2 ;;
  esac
done

EXPORTER="${HOS}/mac/scripts/export_capability_catalog.py"
if [ -z "${HOS}" ] || [ ! -f "${EXPORTER}" ]; then
  echo "[sync][错误] 用法：scripts/sync.sh /path/to/home-agent-os [--check]" >&2
  exit 2
fi

DB="${MARKETPLACE_DB:-${HOME}/database/home-agent-capability-marketplace/marketplace.sqlite3}"
TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

if [ -n "${CHECK}" ]; then
  echo "[sync] 对账：代码 → 临时库 → 与仓库里 catalog 的声明字段比（集市注解不算差异）"
  OUT="${TMP}/out.json"
  python3 "${EXPORTER}" --out "${TMP}/code" >/dev/null
  python3 "${HERE}/server/catalog_cli.py" --db "${TMP}/check.sqlite3" import "${TMP}/code/catalog/capabilities.json" >/dev/null
  python3 "${HERE}/server/catalog_cli.py" --db "${TMP}/check.sqlite3" export --out "${OUT}" >/dev/null
  python3 "${HERE}/tests/catalog-drift.py" "${OUT}" "${HERE}/catalog/capabilities.json"
  exit 0
fi

echo "[sync] 导出（${HOS}）→ ${TMP}"
python3 "${EXPORTER}" --out "${TMP}"
echo "[sync] 入库：${DB}"
python3 "${HERE}/server/catalog_cli.py" --db "${DB}" import "${TMP}/catalog/capabilities.json" \
  --note "sync from home-agent-os $(git -C "${HOS}" rev-parse --short HEAD 2>/dev/null || echo unknown)"
echo "[sync] 回写仓库：catalog/（库导出，含注解）+ capabilities/*.md（代码视图）"
python3 "${HERE}/server/catalog_cli.py" --db "${DB}" export --out "${HERE}/catalog/capabilities.json"
cp "${TMP}/catalog/capabilities.md" "${HERE}/catalog/capabilities.md"
mkdir -p "${HERE}/schema"
cp "${TMP}/schema/catalog.schema.json" "${HERE}/schema/catalog.schema.json"
mkdir -p "${HERE}/capabilities"
rm -f "${HERE}/capabilities/"*.md
cp "${TMP}/capabilities/"*.md "${HERE}/capabilities/"

echo "[sync] 自检"
python3 "${HERE}/tests/catalog-schema.test.py"
python3 -m unittest discover -s "${HERE}/server/tests" -t "${HERE}" >/dev/null && echo "[sync] 服务端测试通过"
if command -v node >/dev/null 2>&1; then
  node --test "${HERE}/tests/"*.test.mjs >/dev/null && echo "[sync] UI 逻辑测试通过"
fi

if [ -d "${HERE}/.git" ]; then
  cd "${HERE}"
  if [ -n "$(git status --porcelain)" ]; then
    git add -A
    commit="${HOS_COMMIT:-$(git -C "${HOS}" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
    git commit -q -m "chore(catalog): 从 home-agent-os ${commit} 同步能力目录 → 库" \
      -m "导出器产出先入库（保留集市注解），再由库导出 catalog/capabilities.json；capabilities/*.md 仍为代码视图。"
    echo "[sync] 已提交（git push 请自行确认）"
  else
    echo "[sync] 目录无变化"
  fi
fi
