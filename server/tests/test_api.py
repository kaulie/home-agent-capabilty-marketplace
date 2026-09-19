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
        marketplace._local.con = con
        self.con = con
        self.addCleanup(con.close)

    def q(self, path: str, **params) -> dict:
        query = {k: [str(v)] for k, v in params.items()}
        status, payload = marketplace.route("GET", path, query, None)
        self.assertEqual(status, 200, payload)
        return payload

    def test_health_and_stats_are_declaration_only(self) -> None:
        self.assertTrue(self.q("/health")["ok"])
        stats = self.q("/api/v1/stats")
        self.assertEqual(stats["service"], marketplace.SERVICE_NAME)
        self.assertGreater(stats["capabilities"], 50)
        for gone in ("live", "declared_not_live", "live_not_declared"):
            self.assertNotIn(gone, stats)

    def test_capabilities_search_and_declaration_filters(self) -> None:
        self.assertGreaterEqual(self.q("/api/v1/capabilities", q="电视")["total"], 1)
        self.assertGreaterEqual(self.q("/api/v1/capabilities", q="asset_ref")["total"], 1)
        self.assertEqual(self.q("/api/v1/capabilities", group="display")["total"], 7)
        self.assertGreaterEqual(self.q("/api/v1/capabilities", service="xiaomi.tv.display")["total"], 1)
        self.assertGreaterEqual(self.q("/api/v1/capabilities", conditional="1")["total"], 1)
        facets = self.q("/api/v1/facets")
        self.assertTrue(facets["groups"] and facets["kinds"] and facets["services"])
        self.assertNotIn("edges", facets)

    def test_capability_detail_and_patch(self) -> None:
        detail = self.q("/api/v1/capabilities/display.audio")["capability"]
        self.assertEqual(detail["capability_id"], "display.audio")
        self.assertEqual(detail["declared_by"], ["xiaomi.tv.display"])
        self.assertIn("events", detail)
        status, payload = marketplace.route(
            "PATCH", "/api/v1/capabilities/display.audio", {}, {"status": "active", "tags": "投屏,音频", "notes": "ok"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["capability"]["tags"], ["投屏", "音频"])
        self.assertEqual(marketplace.route("PATCH", "/api/v1/capabilities/display.audio", {}, {"status": "nope"})[0], 400)
        self.assertEqual(marketplace.route("GET", "/api/v1/capabilities/nope.none", {}, None)[0], 404)

    def test_import_endpoint(self) -> None:
        status, payload = marketplace.route("POST", "/api/v1/catalog:import", {}, {"catalog": CATALOG, "note": "test"})
        self.assertEqual(status, 200, payload)
        self.assertEqual(payload["import"]["added"], [])
        self.assertEqual(marketplace.route("POST", "/api/v1/catalog:import", {}, {"nope": 1})[0], 400)
        self.assertEqual(marketplace.route("POST", "/api/v1/catalog:import", {}, None)[0], 400)

    def test_services_imports_events_export(self) -> None:
        self.assertTrue(self.q("/api/v1/services")["services"])
        self.assertTrue(self.q("/api/v1/imports", limit=5)["imports"])
        exported = self.q("/api/v1/export")
        self.assertEqual(exported["schema"], "home-agent.capability-catalog/v1")
        self.assertTrue(self.q("/api/v1/events", capability_id="display.audio", limit=5)["ok"])


    def test_patch_description_and_keywords(self) -> None:
        status, payload = marketplace.route(
            "PATCH",
            "/api/v1/capabilities/display.audio",
            {},
            {"description": "给电视放音频", "keywords": "投屏，电视"},
        )
        self.assertEqual(status, 200, payload)
        self.assertEqual(payload["capability"]["keywords"], ["投屏", "电视"])
        self.assertEqual(payload["capability"]["description"], "给电视放音频")
        # 打错字段名要立刻报错，而不是静默无效
        code, payload = marketplace.route("PATCH", "/api/v1/capabilities/display.audio", {}, {"descriptoin": "typo"})
        self.assertEqual(code, 400)
        self.assertIn("descriptoin", payload["error"])

    def test_keyword_and_described_filters(self) -> None:
        self.q(
            "/api/v1/capabilities/display.audio",
        ) if False else None
        marketplace.route(
            "PATCH", "/api/v1/capabilities/display.audio", {}, {"description": "给电视放音频", "keywords": "投屏,电视"}
        )
        self.assertEqual(self.q("/api/v1/capabilities", keyword="电视")["total"], 1)
        self.assertGreaterEqual(self.q("/api/v1/capabilities", described="1")["total"], 1)
        self.assertEqual(self.q("/api/v1/capabilities", q="给电视放音频")["total"], 1)
        facets = self.q("/api/v1/facets")
        self.assertIn("电视", [k["name"] for k in facets["keywords"]])


    def test_hosts_endpoints_and_host_filter(self) -> None:
        hosts = self.q("/api/v1/hosts")
        self.assertTrue(hosts["hosts"])
        by_id = {h["host_id"]: h for h in hosts["hosts"]}
        self.assertIn("mac", by_id)
        # 宿主元数据可改
        code, payload = marketplace.route("PATCH", "/api/v1/hosts/mac", {}, {"display_name": "客厅 Mac Edge", "status": "active"})
        self.assertEqual(code, 200, payload)
        self.assertEqual(payload["host"]["display_name"], "客厅 Mac Edge")
        self.assertEqual(payload["host"]["curated"], True)
        self.assertEqual(marketplace.route("PATCH", "/api/v1/hosts/mac", {}, {"typo": 1})[0], 400)
        self.assertEqual(marketplace.route("PATCH", "/api/v1/hosts/nope", {}, {"notes": "x"})[0], 404)
        self.assertEqual(marketplace.route("GET", "/api/v1/hosts/mac", {}, None)[0], 405)
        # 能力侧：按宿主筛 + 人工设置宿主
        self.assertGreaterEqual(self.q("/api/v1/capabilities", host="mac")["total"], 1)
        code, payload = marketplace.route(
            "PATCH", "/api/v1/capabilities/display.audio", {}, {"hosts": "mac, brain"}
        )
        self.assertEqual(code, 200, payload)
        self.assertEqual(payload["capability"]["hosts"], ["brain", "mac"])
        self.assertEqual(payload["capability"]["hosts_source"], "curated")
        self.assertIn("brain", [h["host_id"] for h in self.q("/api/v1/hosts")["hosts"]])
        self.assertGreaterEqual(self.q("/api/v1/capabilities", host="brain")["total"], 1)
        facets = self.q("/api/v1/facets")
        self.assertIn("mac", [h["name"] for h in facets["hosts"]])


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

    def _get(self, path: str):
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
        self.assertTrue(json.loads(body)["count"] >= 1)
        code, body = self._get("/web/index.html")
        self.assertEqual(code, 200)
        self.assertIn(b"<html", body.lower())
        self.assertEqual(self._get("/capabilities/display.audio.md")[0], 200)
        self.assertEqual(self._get("/api/v1/capabilities/nope")[0], 404)


if __name__ == "__main__":
    unittest.main()
