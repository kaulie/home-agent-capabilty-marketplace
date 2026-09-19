"""marketplace.py：能力集市的 HTTP 服务（Python 标准库，无第三方依赖）。

职责：
- **API**（数据源是 SQLite，不读生成好的 JSON）：
    GET  /health
    GET  /api/v1/stats
    GET  /api/v1/capabilities?q=&group=&kind=&edge=&status=&tag=&owner=&live=&has_checker=&sort=&limit=&offset=
    GET  /api/v1/capabilities/{id}
    PATCH /api/v1/capabilities/{id}     改集市自有字段（status/owner/tags/notes）
    GET  /api/v1/facets
    GET  /api/v1/services
    GET  /api/v1/imports?limit=
    GET  /api/v1/events?capability_id=&limit=
    POST /api/v1/catalog:import         导入导出器的 catalog JSON（覆盖生成物字段、保留注解）
    GET  /api/v1/export                 集市导出（含注解）
- **静态**：/ 与 /web/* → UI；/catalog/*、/capabilities/*.md、/schema/* → 仓库里的生成物

为什么用标准库：与项目里其它 py 服务一致（Brain 用 Flask，但这里路由很少），
零依赖 = 部署简单（build.sh 只需 rsync，不需要 pip/venv）。
"""

from __future__ import annotations

import json
import logging
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

import db

log = logging.getLogger("marketplace")

SERVICE_NAME = "home-asset-capabilty-marketplace"
STARTED_AT = time.time()
MIME = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".png": "image/png",
}


class State:
    """进程级状态：DB 路径 + 静态目录。DB 连接按线程各持一份（ThreadingHTTPServer）。"""

    db_path: str = ":memory:"
    web_dir: Path = Path("web")
    static_dir: Path = Path(".")


STATE = State()
_local = threading.local()


def conn() -> sqlite3.Connection:
    """每线程一个连接（sqlite3 连接默认不能跨线程；数据集很小，连接开销可忽略）。"""
    con = getattr(_local, "con", None)
    if con is None:
        con = db.connect(STATE.db_path)
        _local.con = con
    return con


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")


def _int(raw: Any, default: int) -> int:
    try:
        return int(str(raw))
    except (TypeError, ValueError):
        return default


def api_stats(con: sqlite3.Connection) -> dict[str, Any]:
    s = db.stats(con)
    return {
        "ok": True,
        "service": SERVICE_NAME,
        "db": STATE.db_path,
        "schema_version": s["schema_version"],
        "uptime_sec": int(time.time() - STARTED_AT),
        **s,
    }


def route(
    method: str, path: str, query: dict[str, list[str]], body: dict[str, Any] | None
) -> tuple[int, dict[str, Any]]:
    """纯路由：返回 (status, payload)。便于单测直接调（不经 socket）。"""
    con = conn()
    one = lambda k, d="": (query.get(k) or [d])[0]  # noqa: E731


    if path == "/health":
        return 200, {"ok": True, "service": SERVICE_NAME, "uptime_sec": int(time.time() - STARTED_AT),
                     "capabilities": db.stats(con)["capabilities"]}
    if path == "/api/v1/stats":
        return 200, api_stats(con)
    if path == "/api/v1/facets":
        return 200, {"ok": True, **db.facets(con)}
    if path == "/api/v1/services":
        rows = [dict(r) for r in con.execute("select * from services order by service_id")]
        for row in rows:
            row["capabilities"] = [r[0] for r in con.execute(
                "select capability_id from service_capabilities where service_id=? order by capability_id",
                (row["service_id"],))]
        return 200, {"ok": True, "count": len(rows), "services": rows}
    if path == "/api/v1/imports":
        items = db.list_imports(con, limit=_int(one("limit", "20"), 20))
        return 200, {"ok": True, "count": len(items), "imports": items}
    if path == "/api/v1/events":
        items = db.list_events(con, capability_id=one("capability_id"), limit=_int(one("limit", "50"), 50))
        return 200, {"ok": True, "count": len(items), "events": items}
    if path == "/api/v1/export":
        return 200, db.export_catalog(con)
    if path == "/api/v1/catalog:import" or path == "/api/v1/import":
        if method != "POST":
            return 405, {"ok": False, "error": "POST required"}
        if not isinstance(body, dict):
            return 400, {"ok": False, "error": "缺少 catalog JSON body"}
        catalog = body.get("catalog") if isinstance(body.get("catalog"), dict) else body
        if not isinstance(catalog.get("capabilities"), list):
            return 400, {"ok": False, "error": "catalog.capabilities 必须是数组"}
        result = db.import_catalog(con, catalog, note=str(body.get("note") or "http"))
        return 200, {"ok": True, "import": result}

    if path == "/api/v1/capabilities":
        result = db.list_capabilities(
            con,
            q=one("q"), group=one("group"), kind=one("kind"), edge=one("edge"), status=one("status"),
            tag=one("tag"), owner=one("owner"), live=one("live"),
            has_checker=one("has_checker"), sort=one("sort"),
            limit=_int(one("limit", "500"), 500), offset=_int(one("offset", "0"), 0),
            in_catalog=(one("in_catalog", "1") not in ("0", "false")),
        )
        result["ok"] = True
        return 200, result

    if path.startswith("/api/v1/capabilities/"):
        cid = unquote(path[len("/api/v1/capabilities/"):]).strip()
        if method == "GET":
            cap = db.get_capability(con, cid)
            return (200, {"ok": True, "capability": cap}) if cap else (404, {"ok": False, "error": "not found"})
        if method == "PATCH":
            if not isinstance(body, dict):
                return 400, {"ok": False, "error": "body 必须是 JSON 对象"}
            try:
                cap = db.annotate(con, cid, body, actor=str(body.get("_actor") or "api"))
            except ValueError as e:
                return 400, {"ok": False, "error": str(e)}
            return (200, {"ok": True, "capability": cap}) if cap else (404, {"ok": False, "error": "not found"})
        return 405, {"ok": False, "error": "GET/PATCH only"}

    return 404, {"ok": False, "error": f"未知路径 {path}"}


class Handler(BaseHTTPRequestHandler):
    server_version = "home-asset-marketplace/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
        log.info("%s - %s", self.address_string(), fmt % args)

    # --- 基础 -------------------------------------------------------------
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _payload(self, status: int, obj: Any) -> None:
        self._send(status, _json_bytes(obj), "application/json; charset=utf-8")

    def _read_body(self) -> dict[str, Any] | None:
        length = _int(self.headers.get("Content-Length"), 0)
        if length <= 0:
            return None
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8", "replace"))
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send(204, b"", "text/plain")

    def do_GET(self) -> None:  # noqa: N802
        self._handle("GET")

    def do_HEAD(self) -> None:  # noqa: N802
        self._handle("GET")

    def do_POST(self) -> None:  # noqa: N802
        self._handle("POST")

    def do_PATCH(self) -> None:  # noqa: N802
        self._handle("PATCH")

    # --- 路由 -------------------------------------------------------------
    def _handle(self, method: str) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        query = parse_qs(parsed.query)
        if path == "/health" or path.startswith("/api/"):
            body = self._read_body() if method in ("POST", "PATCH") else None
            try:
                status, payload = route(method, path, query, body)
            except Exception as e:  # noqa: BLE001 — 服务不能因为一个请求挂掉
                log.exception("route failed: %s %s", method, path)
                status, payload = 500, {"ok": False, "error": f"internal error: {e}"}
            self._payload(status, payload)
            return
        self._serve_static(path)

    def _serve_static(self, path: str) -> None:
        if path.startswith("/web/"):
            base, rel = STATE.web_dir, path[len("/web/") :]
        elif path in ("/", "/index.html"):
            base, rel = STATE.static_dir, "index.html"
        elif path.startswith(("/catalog/", "/capabilities/", "/schema/")):
            base, rel = STATE.static_dir, path.lstrip("/")
        else:
            self._payload(404, {"ok": False, "error": f"未知路径 {path}"})
            return
        target = (base / rel).resolve()
        try:
            target.relative_to(base.resolve())
        except ValueError:
            self._payload(404, {"ok": False, "error": "bad path"})
            return
        if not target.is_file():
            self._payload(404, {"ok": False, "error": f"not found: {path}"})
            return
        self._send(200, target.read_bytes(), MIME.get(target.suffix.lower(), "application/octet-stream"))


def serve(*, db_path: str, host: str, port: int, web_dir: Path, static_dir: Path) -> None:
    """起服务（阻塞）。DB 在建连时就初始化 schema（空库也能起来）。"""
    STATE.db_path = str(db_path)
    STATE.web_dir = Path(web_dir)
    STATE.static_dir = Path(static_dir)
    conn().commit()  # 触发 schema 初始化 + 目录创建（早失败早发现）
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    srv = ThreadingHTTPServer((host, int(port)), Handler)
    log.info("marketplace listening on %s:%s db=%s sqlite=%s", host, port, db_path, sqlite3.sqlite_version)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        log.info("interrupted")
    finally:
        srv.server_close()

