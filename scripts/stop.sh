#!/usr/bin/env bash
# 停止能力集市服务（TERM → 15s → KILL）。兜底：pid 文件丢了按端口找 catalog_cli serve。
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SELF_RUNTIME_DIR="$(cd "${DIR}/.." && pwd)"
RUNTIME_DIR="${SELF_RUNTIME_DIR}"
PID_FILE="${RUNTIME_DIR}/backend/runtime.pid"
PORT="${MARKETPLACE_PORT:-}"
if [ -z "${PORT}" ]; then
  env_file="${SELF_RUNTIME_DIR}/backend/.env"
  if [ -f "${env_file}" ]; then
    PORT="$(awk -F= '/^[[:space:]]*MARKETPLACE_PORT[[:space:]]*=/{gsub(/[[:space:]\"]/,"",$2); v=$2} END{print v}' "${env_file}" 2>/dev/null || true)"
  fi
fi
if [ -z "${PORT}" ]; then PORT=4250; fi  # 契约口；刻意不读继承来的 SERVICE_PORT（那是别的服务的）
log() { echo "[stop] $*"; }

PIDS=()
if [ -f "${PID_FILE}" ]; then
  pid="$(tr -d '[:space:]' < "${PID_FILE}" || true)"
  if [ -n "${pid}" ] && kill -0 "${pid}" 2>/dev/null; then
    PIDS+=("${pid}")
  else
    log "pid 文件里的 ${pid:-?} 已不存在，清理"
  fi
  rm -f "${PID_FILE}"
fi

if [ "${#PIDS[@]}" -eq 0 ] && command -v lsof >/dev/null 2>&1; then
  for cand in $(lsof -nP -iTCP:"${PORT}" -sTCP:LISTEN -t 2>/dev/null || true); do
    cmd="$(ps -o command= -ww -p "${cand}" 2>/dev/null || true)"
    case "${cmd}" in
      *catalog_cli.py*serve*) log "兜底：端口 ${PORT} 上的 pid=${cand} 是能力集市"; PIDS+=("${cand}") ;;
    esac
  done
fi

if [ "${#PIDS[@]}" -eq 0 ]; then
  log "没有运行中的能力集市服务"
  exit 0
fi

for pid in "${PIDS[@]}"; do
  log "TERM → pid=${pid}"
  kill "${pid}" 2>/dev/null || true
  for _ in $(seq 1 30); do
    kill -0 "${pid}" 2>/dev/null || break
    sleep 0.5
  done
  if kill -0 "${pid}" 2>/dev/null; then
    log "15s 内未退出，KILL → pid=${pid}"
    kill -9 "${pid}" 2>/dev/null || true
  fi
done
log "已停止"
