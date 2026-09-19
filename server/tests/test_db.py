"""marketplace 数据库单测（标准库 unittest）：只测**声明与策展**，不测实时状态。

跑法：python3 -m unittest discover -s server/tests -t .
"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SERVER = REPO / "server"
if str(SERVER) not in sys.path:
    sys.path.insert(0, str(SERVER))

import db  # noqa: E402

CATALOG = json.loads((REPO / "catalog" / "capabilities.json").read_text(encoding="utf-8"))


def fresh_db():
    return db.connect(tempfile.mktemp(suffix=".sqlite3"))


class ImportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.con = fresh_db()
        self.addCleanup(self.con.close)

    def test_import_then_query_matches_catalog(self) -> None:
        result = db.import_catalog(self.con, CATALOG)
        self.assertGreater(result["counts"]["capabilities"], 50)
        self.assertEqual(len(result["added"]), result["counts"]["capabilities"])
        self.assertEqual(db.list_capabilities(self.con, limit=1000)["total"], result["counts"]["capabilities"])

    def test_reimport_is_idempotent_and_reports_contract_changes(self) -> None:
        db.import_catalog(self.con, CATALOG)
        again = db.import_catalog(self.con, CATALOG)
        self.assertEqual((again["added"], again["changed"], again["removed"]), ([], [], []))
        tampered = copy.deepcopy(CATALOG)
        for cap in tampered["capabilities"]:
            if cap["capability_id"] == "display.audio":
                cap["definition"]["typical_triggers"] = ["被改过的触发语"]
        res = db.import_catalog(self.con, tampered)
        self.assertEqual(res["changed"], ["display.audio"])

    def test_marketplace_annotations_survive_reimport(self) -> None:
        """核心保证：集市自己维护的字段，重导入不许覆盖。"""
        db.import_catalog(self.con, CATALOG)
        db.annotate(self.con, "display.audio", {"owner": "gaolei", "tags": "投屏,音频", "notes": "电视出声确认过"})
        db.import_catalog(self.con, CATALOG)
        cap = db.get_capability(self.con, "display.audio")
        self.assertEqual(cap["owner"], "gaolei")
        self.assertEqual(cap["tags"], ["投屏", "音频"])
        self.assertTrue(cap["reviewed_at"])
        self.assertTrue(any(e["field"] == "owner" for e in cap["events"]))

    def test_removed_capability_is_soft_deleted_and_restored(self) -> None:
        catalog = copy.deepcopy(CATALOG)
        db.import_catalog(self.con, catalog)
        catalog["capabilities"] = [c for c in catalog["capabilities"] if c["capability_id"] != "clock.now"]
        res = db.import_catalog(self.con, catalog)
        self.assertIn("clock.now", res["removed"])
        self.assertFalse(db.get_capability(self.con, "clock.now")["in_catalog"])
        res2 = db.import_catalog(self.con, CATALOG)
        self.assertIn("clock.now", res2["restored"])

    def test_search_group_and_declaration_queries(self) -> None:
        db.import_catalog(self.con, CATALOG)
        self.assertGreaterEqual(db.list_capabilities(self.con, q="电视")["total"], 1)
        self.assertGreaterEqual(db.list_capabilities(self.con, q="电视 音频")["total"], 1)
        self.assertGreaterEqual(db.list_capabilities(self.con, q="asset_ref")["total"], 1)
        self.assertEqual(db.list_capabilities(self.con, group="display")["total"], 7)
        self.assertTrue(db.list_capabilities(self.con, kind="system")["total"] >= 1)
        # 声明维度：条件挂载 / 有服务归属 / 有文档包
        conditional = db.list_capabilities(self.con, conditional=1)
        self.assertGreaterEqual(conditional["total"], 1)
        self.assertTrue(all(c["conditional_lists"] for c in conditional["capabilities"]))
        svc = db.list_capabilities(self.con, service="xiaomi.tv.display")
        self.assertGreaterEqual(svc["total"], 1)
        self.assertTrue(all("xiaomi.tv.display" in c["declared_by"] for c in svc["capabilities"]))

    def test_annotate_validation_and_search_blob(self) -> None:
        db.import_catalog(self.con, CATALOG)
        with self.assertRaises(ValueError):
            db.annotate(self.con, "clock.now", {"status": "whatever"})
        db.annotate(self.con, "clock.now", {"owner": "gaolei", "notes": "只在整点报时用"})
        self.assertEqual(db.list_capabilities(self.con, q="整点报时")["total"], 1)
        self.assertEqual(db.list_capabilities(self.con, owner="gaolei")["total"], 1)

    def test_stats_facets_and_export_are_declaration_only(self) -> None:
        db.import_catalog(self.con, CATALOG)
        s = db.stats(self.con)
        for key in ("capabilities", "services", "packages", "conditional", "with_preflight", "with_service", "annotated"):
            self.assertIn(key, s)
        for gone in ("live", "declared_not_live", "live_not_declared"):
            self.assertNotIn(gone, s, "集市不再登记实时状态")
        f = db.facets(self.con)
        self.assertTrue(f["groups"] and f["kinds"] and f["services"])
        self.assertNotIn("edges", f)
        exported = db.export_catalog(self.con)
        self.assertEqual(exported["summary"]["capabilities"], len(CATALOG["capabilities"]))
        cap = next(c for c in exported["capabilities"] if c["capability_id"] == "display.audio")
        self.assertIn("declaration", cap)
        self.assertEqual(cap["declaration"]["declared_by"], ["xiaomi.tv.display"])
        for gone in ("in_live", "live", "providers", "reconcile"):
            self.assertNotIn(gone, cap, "导出里不该有实时字段")


    def test_description_and_keywords_are_editable_searchable_filterable(self) -> None:
        """描述与关键字是**人工维护**字段：可编辑、进搜索、能筛，且重导入不丢。"""
        db.import_catalog(self.con, CATALOG)
        db.annotate(
            self.con,
            "display.audio",
            {"description": "把已有音频交给小米电视出声，不负责投图。", "keywords": "投屏，电视 音频, 看电视"},
        )
        cap = db.get_capability(self.con, "display.audio")
        self.assertEqual(cap["keywords"], ["投屏", "电视", "看电视", "音频"])  # 去重 + 排序
        self.assertIn("小米电视", cap["description"])
        # 重导入不覆盖（这是集市字段的意义）
        db.import_catalog(self.con, CATALOG)
        again = db.get_capability(self.con, "display.audio")
        self.assertEqual(again["keywords"], cap["keywords"])
        self.assertEqual(again["description"], cap["description"])
        # 搜索命中描述与关键字
        self.assertIn("display.audio", [c["capability_id"] for c in db.list_capabilities(self.con, q="不负责投图")["capabilities"]])
        self.assertIn("display.audio", [c["capability_id"] for c in db.list_capabilities(self.con, q="看电视")["capabilities"]])
        # 按关键字筛 / 按「有描述」筛
        kw = db.list_capabilities(self.con, keyword="电视")
        self.assertEqual([c["capability_id"] for c in kw["capabilities"]], ["display.audio"])
        self.assertEqual(db.list_capabilities(self.con, keyword="不存在的关键字")["total"], 0)
        self.assertEqual(db.list_capabilities(self.con, described=1)["total"], 1)
        # 统计 + facets（人工设定的关键字可当筛选下拉）
        s = db.stats(self.con)
        self.assertEqual((s["described"], s["with_keywords"], s["annotated"]), (1, 1, 1))
        self.assertIn("电视", [k["name"] for k in db.facets(self.con)["keywords"]])
        # 审计留痕
        self.assertTrue(any(e["field"] == "keywords" for e in cap["events"]))
        self.assertTrue(any(e["field"] == "description" for e in cap["events"]))

    def test_description_and_keywords_validation(self) -> None:
        db.import_catalog(self.con, CATALOG)
        with self.assertRaises(ValueError):
            db.annotate(self.con, "clock.now", {"description": "x" * 2001})
        with self.assertRaises(ValueError):
            db.annotate(self.con, "clock.now", {"keywords": [f"k{i}" for i in range(21)]})
        with self.assertRaises(ValueError):
            db.annotate(self.con, "clock.now", {"keywords": ["y" * 41]})


    HOST_CATALOG = {
        "schema": "home-agent.capability-catalog/v1",
        "source": {"repo": "test", "commit": "deadbeef", "edge": "mac_edge"},
        "capabilities": [
            {
                "capability_id": "display.audio",
                "kind": "output", "composition": "atomic", "group": "display",
                "in_ads": True, "declared_by": ["xiaomi.tv.display"], "packages": [],
                "runs_on": ["mac"],
                "definition": {"kind": "output", "composition": "atomic", "group": "display"},
            },
            {
                "capability_id": "asset.inventory",
                "kind": "system", "composition": "atomic", "group": "asset",
                "in_ads": True, "declared_by": [], "packages": [],
                "runs_on": ["brain"],
                "definition": {"kind": "system", "composition": "atomic", "group": "asset"},
            },
        ],
    }

    def test_hosts_registry_seeded_from_code_facts(self) -> None:
        """宿主注册表从「代码声明的适用宿主」自动登记，并给可读名。"""
        db.import_catalog(self.con, self.HOST_CATALOG)
        hosts = {h["host_id"]: h for h in db.list_hosts(self.con)}
        self.assertEqual(sorted(hosts), ["brain", "mac"])
        self.assertEqual(hosts["mac"]["display_name"], "Mac Edge（本机 macOS）")
        self.assertEqual(hosts["mac"]["kind"], "edge")
        self.assertEqual(hosts["brain"]["capabilities"], 1)
        self.assertFalse(hosts["mac"]["curated"])
        cap = db.get_capability(self.con, "display.audio")
        self.assertEqual(cap["runs_on"], ["mac"])
        self.assertEqual(cap["hosts_effective"], ["mac"])
        self.assertEqual(cap["hosts_source"], "code")
        s = db.stats(self.con)
        self.assertEqual((s["with_hosts"], s["hosts"], s["hosts_curated"]), (2, 2, 0))
        self.assertEqual([h["name"] for h in db.facets(self.con)["hosts"]], ["brain", "mac"])

    def test_curated_hosts_override_code_and_survive_import(self) -> None:
        """人工设置的适用宿主优先于代码事实，且重导入不被覆盖；新宿主 id 会自动登记。"""
        db.import_catalog(self.con, self.HOST_CATALOG)
        db.annotate(self.con, "display.audio", {"hosts": "mac, 电视盒子"})
        cap = db.get_capability(self.con, "display.audio")
        self.assertEqual(cap["hosts"], ["mac", "电视盒子"])
        self.assertEqual(cap["hosts_source"], "curated")
        self.assertIn("电视盒子", [h["host_id"] for h in db.list_hosts(self.con)])
        db.import_catalog(self.con, self.HOST_CATALOG)
        self.assertEqual(db.get_capability(self.con, "display.audio")["hosts"], ["mac", "电视盒子"])
        self.assertIn("display.audio", [c["capability_id"] for c in db.list_capabilities(self.con, host="电视盒子")["capabilities"]])
        self.assertIn("display.audio", [c["capability_id"] for c in db.list_capabilities(self.con, host="mac")["capabilities"]])
        self.assertEqual(db.list_capabilities(self.con, host="brain")["total"], 1)

    def test_host_metadata_is_editable_and_survives_import(self) -> None:
        """宿主本身也可设置（显示名/分类/备注/状态），导入不动人工改过的元数据。"""
        db.import_catalog(self.con, self.HOST_CATALOG)
        host = db.annotate_host(self.con, "mac", {"display_name": "客厅 Mac Edge", "kind": "edge", "notes": "24h 在跑", "status": "active"})
        self.assertEqual(host["display_name"], "客厅 Mac Edge")
        self.assertTrue(host["curated"])
        db.import_catalog(self.con, self.HOST_CATALOG)
        again = {h["host_id"]: h for h in db.list_hosts(self.con)}["mac"]
        self.assertEqual(again["display_name"], "客厅 Mac Edge")
        self.assertEqual(again["notes"], "24h 在跑")
        self.assertTrue(any(e["capability_id"] == "host:mac" for e in db.list_events(self.con, limit=50)))
        with self.assertRaises(ValueError):
            db.annotate_host(self.con, "mac", {"status": "nope"})

    def test_hosts_validation(self) -> None:
        db.import_catalog(self.con, self.HOST_CATALOG)
        with self.assertRaises(ValueError):
            db.annotate(self.con, "display.audio", {"hosts": [f"h{i}" for i in range(21)]})
        with self.assertRaises(ValueError):
            db.annotate(self.con, "display.audio", {"hosts": ["x" * 41]})

    def test_hosts_are_searchable_by_id_and_display_name(self) -> None:
        db.import_catalog(self.con, self.HOST_CATALOG)
        self.assertIn("display.audio", [c["capability_id"] for c in db.list_capabilities(self.con, q="mac")["capabilities"]])
        self.assertIn("display.audio", [c["capability_id"] for c in db.list_capabilities(self.con, q="Mac Edge")["capabilities"]])


if __name__ == "__main__":
    unittest.main()
