#!/usr/bin/env bash
#
# 同步能力目录：从本仓 plugins/ + declarations/ 导出 → 导入 marketplace 数据库 → 回写 catalog。
#
#   scripts/sync.sh          # 导出 + 入库 + 回写 + 自检 + 提交
#   scripts/sync.sh --check  # 只对账（CI）：与仓库 catalog 的声明字段比
#
# 集市是声明权威，不读 home-agent-os / brain / gateway。
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECK=""
for arg in "$@"; do
  case "$arg" in
    --check) CHECK="--check" ;;
    *) echo "[sync][错误] 未知参数 $arg（已不再接受 home-agent-os 路径）" >&2; exit 2 ;;
  esac
done

EXPORTER="${HERE}/scripts/export_catalog.py"
if [ ! -f "${EXPORTER}" ]; then
  echo "[sync][错误] 缺少 ${EXPORTER}" >&2
  exit 2
fi

DB="${MARKETPLACE_DB:-${HOME}/database/home-agent-capability-marketplace/marketplace.sqlite3}"
TMP="$(mktemp -d)"
trap 'rm -rf "${TMP}"' EXIT

if [ -n "${CHECK}" ]; then
  echo "[sync] 对账：本仓声明 → 临时库 → 与仓库 catalog 比声明字段"
  OUT="${TMP}/out.json"
  python3 "${EXPORTER}" --out "${TMP}/code" >/dev/null
  python3 "${HERE}/server/catalog_cli.py" --db "${TMP}/check.sqlite3" import "${TMP}/code/catalog/capabilities.json" >/dev/null
  python3 "${HERE}/server/catalog_cli.py" --db "${TMP}/check.sqlite3" export --out "${OUT}" >/dev/null
  python3 "${HERE}/tests/catalog-drift.py" "${OUT}" "${HERE}/catalog/capabilities.json"
  exit 0
fi

echo "[sync] 导出（本仓 plugins/ + declarations/）→ ${TMP}"
python3 "${EXPORTER}" --out "${TMP}"
echo "[sync] 入库：${DB}"
python3 "${HERE}/server/catalog_cli.py" --db "${DB}" import "${TMP}/catalog/capabilities.json" \
  --note "sync from marketplace plugins $(git -C "${HERE}" rev-parse --short HEAD 2>/dev/null || echo unknown)"
echo "[sync] 回写仓库：catalog/ + capabilities/*.md"
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
    commit="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
    git commit -q -m "chore(catalog): 从本仓声明同步能力目录 → 库" \
      -m "plugins/ + declarations/ 导出后入库（保留集市注解），再由库导出 catalog/capabilities.json。"
    echo "[sync] 已提交（git push 请自行确认）"
  else
    echo "[sync] 目录无变化"
  fi
fi
