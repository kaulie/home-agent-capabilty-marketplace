#!/usr/bin/env bash
#
# 启动能力集市服务（agent-control-plane-deployment 规范）。
#
# 平台调用：cwd = runtimeDir，注入 PORT / SERVICE_PORT / RUNTIME_DIR / APP_VERSION。
# 契约：port=4250、health_url=http://127.0.0.1:4250/health（服务自带 /health）。
#
# 数据库**在代码与 runtime 之外**：默认 ~/database/home-agent-capability-marketplace/marketplace.sqlite3
# （与 Brain 的 BRAIN_DATA_DIR 同款约定）—— 部署 rsync --delete 不会碰它。
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SELF_RUNTIME_DIR="$(cd "${DIR}/.." && pwd)"
APP_VERSION="${APP_VERSION:-dev}"

log() { echo "[start] $*"; }
warn() { echo "[start][警告] $*" >&2; }
die() { echo "[start][错误] $*" >&2; exit 1; }

if [ -n "${RUNTIME_DIR:-}" ] && [ "${RUNTIME_DIR}" != "${SELF_RUNTIME_DIR}" ]; then
  warn "忽略继承来的 RUNTIME_DIR=${RUNTIME_DIR}，按脚本位置用 ${SELF_RUNTIME_DIR}"
fi
RUNTIME_DIR="${SELF_RUNTIME_DIR}"
BACKEND_DIR="${RUNTIME_DIR}/backend"
ENV_FILE="${BACKEND_DIR}/.env"
PID_FILE="${BACKEND_DIR}/runtime.pid"
LOG_FILE="${BACKEND_DIR}/server.log"

# 端口：MARKETPLACE_PORT(shell) > backend/.env > SERVICE_PORT > 4250
PORT="${MARKETPLACE_PORT:-}"
if [ -z "${PORT}" ] && [ -f "${ENV_FILE}" ]; then
  PORT="$(awk -F= '/^[[:space:]]*MARKETPLACE_PORT[[:space:]]*=/{gsub(/[[:space:]\"]/,"",$2); v=$2} END{print v}' "${ENV_FILE}" 2>/dev/null || true)"
fi
if [ -z "${PORT}" ]; then PORT="${SERVICE_PORT:-4250}"; fi

mkdir -p "${BACKEND_DIR}"
if [ ! -f "${ENV_FILE}" ]; then
  warn "没有 ${ENV_FILE}：用默认库 ~/database/home-agent-capability-marketplace/marketplace.sqlite3"
  umask 077
  : > "${ENV_FILE}"
fi
chmod 600 "${ENV_FILE}" 2>/dev/null || true
set -a
# shellcheck disable=SC1090
. "${ENV_FILE}"
set +a

MARKETPLACE_DB="${MARKETPLACE_DB:-${HOME}/database/home-agent-capability-marketplace/marketplace.sqlite3}"
MARKETPLACE_HOST="${MARKETPLACE_HOST:-0.0.0.0}"
export MARKETPLACE_DB MARKETPLACE_HOST MARKETPLACE_PORT="${PORT}"
mkdir -p "$(dirname "${MARKETPLACE_DB}")"

if [ -f "${PID_FILE}" ]; then
  old="$(tr -d '[:space:]' < "${PID_FILE}" || true)"
  if [ -n "${old}" ] && kill -0 "${old}" 2>/dev/null; then
    log "已在运行 pid=${old}"
    exit 0
  fi
  rm -f "${PID_FILE}"
fi

if command -v lsof >/dev/null 2>&1; then
  holder="$(lsof -nP -iTCP:"${PORT}" -sTCP:LISTEN -t 2>/dev/null | head -1 || true)"
  if [ -n "${holder}" ]; then
    die "端口 ${PORT} 已被 pid=${holder} 占用：$(ps -o command= -ww -p "${holder}" 2>/dev/null | head -c 160)"
  fi
fi

command -v python3 >/dev/null 2>&1 || die "没有 python3"
[ -f "${RUNTIME_DIR}/server/catalog_cli.py" ] || die "缺少 server/catalog_cli.py（发版包内容不完整？）"

log "启动 部署版本=${APP_VERSION} 监听=0.0.0.0:${PORT} 数据库=${MARKETPLACE_DB} 健康=http://127.0.0.1:${PORT}/health"
cd "${RUNTIME_DIR}"
nohup python3 server/catalog_cli.py serve --host "${MARKETPLACE_HOST}" --port "${PORT}" --web "${RUNTIME_DIR}/web" --static "${RUNTIME_DIR}" \
  >> "${LOG_FILE}" 2>&1 < /dev/null &
echo $! > "${PID_FILE}"
pid="$(cat "${PID_FILE}")"

for _ in $(seq 1 40); do
  if ! kill -0 "${pid}" 2>/dev/null; then
    rm -f "${PID_FILE}"
    echo "[start][错误] 进程已退出，最近日志：" >&2
    tail -20 "${LOG_FILE}" >&2 || true
    exit 1
  fi
  if curl -fsS -m 2 "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
    log "启动成功 pid=${pid} 数据库=${MARKETPLACE_DB} 日志=${LOG_FILE}"
    exit 0
  fi
  sleep 0.5
done

echo "[start][错误] 20s 内 /health 未就绪，最近日志：" >&2
tail -20 "${LOG_FILE}" >&2 || true
kill "${pid}" 2>/dev/null || true
rm -f "${PID_FILE}"
exit 1
