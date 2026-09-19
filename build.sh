#!/usr/bin/env bash
#
# 打包能力集市 —— 遵循 agent-control-plane-deployment 规范。
#
# 约定：cwd = 仓库根、APP_VERSION = <8 位短 hash>；产出 outputs/，必须含 scripts/restart.sh。
# 纯 Python 标准库 → 不需要 pip/venv：这里只做「语法检查 + 单测 + 拷贝」。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT}"

export PATH="/usr/local/bin:/opt/homebrew/bin:${PATH}"
VERSION="${APP_VERSION:-dev}"
OUT="${ROOT}/outputs"

command -v python3 >/dev/null 2>&1 || { echo "[build][错误] 本机没有 python3" >&2; exit 1; }
[ -f "${ROOT}/scripts/restart.sh" ] || { echo "[build][错误] 缺少 scripts/restart.sh（平台硬性要求）" >&2; exit 1; }
[ -f "${ROOT}/server/catalog_cli.py" ] || { echo "[build][错误] 缺少 server/catalog_cli.py" >&2; exit 1; }

echo "[build] home-asset-capability-marketplace version=${VERSION}"
echo "[build] 语法检查 + 单测"
python3 -m compileall -q server >/dev/null
python3 -m unittest discover -s server/tests -t . >/dev/null
python3 tests/catalog-schema.test.py >/dev/null

rm -rf "${OUT}"
mkdir -p "${OUT}/bin" "${OUT}/scripts"
cp -R "${ROOT}/server" "${ROOT}/web" "${ROOT}/catalog" "${ROOT}/capabilities" "${ROOT}/schema" "${ROOT}/tests" "${OUT}/"
cp "${ROOT}/bin/marketplace" "${OUT}/bin/marketplace"
cp "${ROOT}/README.md" "${OUT}/README.md" 2>/dev/null || true
cp "${ROOT}/scripts/start.sh" "${ROOT}/scripts/stop.sh" "${ROOT}/scripts/restart.sh" "${ROOT}/scripts/sync.sh" "${OUT}/scripts/"
cp "${ROOT}/index.html" "${OUT}/index.html"
[ -f "${ROOT}/.env.example" ] && cp "${ROOT}/.env.example" "${OUT}/.env.example"
find "${OUT}" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
chmod +x "${OUT}/scripts/"*.sh
echo "[build] outputs 就绪："
ls -1 "${OUT}" "${OUT}/scripts" | sed 's/^/  /'
