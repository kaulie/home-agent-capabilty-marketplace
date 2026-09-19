"""marketplace API 单测：直接调 route()（不经 socket）+ 一次真 socket 冒烟。"""

from __future__ import annotations

import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

SERVER = Path(__file__).resolve().parents[1]
if str(SERVER) not in sys.path:
    sys.path.insert(0, str(SERVER))

import db  # noqa: E402
import marketplace  # noqa: E402

REPO = SERVER.parent
CATALOG = json.loads((REPO / "catalog" / "capabilities.json").read_text(encoding="utf-8"))


class RouteTest(unittest.TestCase):
    def setUp(self) -> None:
        con = db.connect(tempfile.mktemp(suffix=".sqlite3"))
        db.import_catalog(con, CATALOG)
        con.commit()
        marketplace.STATE.db_path = str(con.execute("pragma database_list").fetchone()[2])
        marketplace._local.con = con  # 让 route() 直接用这个测试库
        self.con = con
        self.addCleanup(con.close)

    def q(self, path: str, **params) -> dict:
        query = {k: [str(v)] for k, v in params.items()}
        status, payload = marketplace.route("GET", path, query, None)
        self.assertEqual(status, 200, payload)
        return payload

    def test_health_and_stats(self) -> None:
        self.assertTrue(self.q("/health")["ok"])
        stats = self.q("/api/v1/stats")
        self.assertEqual(stats["service"], marketplace.SERVICE_NAME)
        self.assertTrue(stats["schema_version"])
        self.assertGreater(stats["capabilities"], 50)

    def test_capabilities_search_group_live(self) -> None:
        self.assertGreaterEqual(self.q("/api/v1/capabilities", q="电视")["total"], 1)
        self.assertEqual(self.q("/api/v1/capabilities", group="display")["total"], 7)
        ids = [c["capability_id"] for c in self.q("/api/v1/capabilities", live="live_not_declared")["capabilities"]]
        self.assertEqual(sorted(ids), ["display.audio.control", "map.route.estimate", "xiaodu.control", "xiaodu.play"])
        self.assertGreaterEqual(self.q("/api/v1/capabilities", q="asset_ref")["total"], 1)
        self.assertGreaterEqual(self.q("/api/v1/capabilities", edge="客厅 · Mac Edge")["total"], 40)
        facets = self.q("/api/v1/facets")
        self.assertTrue(facets["groups"] and facets["kinds"] and facets["edges"])

    def test_capability_detail_and_patch(self) -> None:
        detail = self.q("/api/v1/capabilities/display.audio")["capability"]
        self.assertEqual(detail["capability_id"], "display.audio")
        self.assertTrue(detail["declared_by"])
        self.assertIn("events", detail)
        status, payload = marketplace.route(
            "PATCH", "/api/v1/capabilities/display.audio", {}, {"status": "active", "tags": "投屏,音频", "notes": "ok"}
        )
        self.assertEqual(status, 200)
        cap = payload["capability"]
        self.assertEqual(cap["tags"], ["投屏", "音频"])
        self.assertEqual(cap["notes"], "ok")
        status, _ = marketplace.route("PATCH", "/api/v1/capabilities/display.audio", {}, {"status": "nope"})
        self.assertEqual(status, 400)
        status, _ = marketplace.route("GET", "/api/v1/capabilities/nope.none", {}, None)
        self.assertEqual(status, 404)

    def test_import_endpoint(self) -> None:
        status, payload = marketplace.route("POST", "/api/v1/catalog:import", {}, {"catalog": CATALOG, "note": "test"})
        self.assertEqual(status, 200, payload)
        self.assertEqual(payload["import"]["added"], [])
        self.assertEqual(marketplace.route("POST", "/api/v1/catalog:import", {}, {"nope": 1})[0], 400)
        self.assertEqual(marketplace.route("POST", "/api/v1/catalog:import", {}, None)[0], 400)

    def test_services_imports_events_export(self) -> None:
        self.assertTrue(self.q("/api/v1/services")["services"])
        self.assertTrue(self.q("/api/v1/imports", limit=5)["imports"])
        self.assertEqual(self.q("/api/v1/export")["schema"], "home-agent.capability-catalog/v1")
        self.assertTrue(self.q("/api/v1/events", capability_id="display.audio", limit=5)["ok"])


class SocketSmokeTest(unittest.TestCase):
    """真起一次 HTTP 服务：静态页与 API 都能通过 socket 拿到。"""

    @classmethod
    def setUpClass(cls) -> None:
        db_path = str(Path(tempfile.mkdtemp()) / "smoke.sqlite3")
        con = db.connect(db_path)
        db.import_catalog(con, CATALOG)
        con.commit()
        marketplace.STATE.db_path = db_path
        marketplace.STATE.web_dir = REPO / "web"
        marketplace.STATE.static_dir = REPO
        marketplace._local.con = con
        cls.con = con
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), marketplace.Handler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.con.close()

    def _get(self, path: str) -> tuple[int, bytes]:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=5) as resp:
                return int(resp.status), resp.read()
        except urllib.error.HTTPError as e:
            return int(e.code), e.read()

    def test_health_api_and_static(self) -> None:
        code, body = self._get("/health")
        self.assertEqual(code, 200)
        self.assertTrue(json.loads(body)["ok"])
        code, body = self._get("/api/v1/capabilities?q=%E7%94%B5%E8%A7%86&limit=5")
        self.assertEqual(code, 200)
        payload = json.loads(body)
        self.assertTrue(payload["ok"] and payload["count"] >= 1)
        code, body = self._get("/web/index.html")
        self.assertEqual(code, 200)
        self.assertIn(b"<html", body.lower())
        code, _ = self._get("/capabilities/display.audio.md")
        self.assertEqual(code, 200)
        self.assertEqual(self._get("/api/v1/capabilities/nope")[0], 404)


if __name__ == "__main__":
    unittest.main()

