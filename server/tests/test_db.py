"""marketplace 数据库与 API 的单测（标准库 unittest；不依赖网络外的服务）。

跑法：python3 -m unittest discover -s server/tests -t .  （见 README/CI）
"""

from __future__ import annotations

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
import marketplace  # noqa: E402

CATALOG = json.loads((REPO / "catalog" / "capabilities.json").read_text(encoding="utf-8"))


def fresh_db() -> "db.sqlite3.Connection":
    return db.connect(tempfile.mktemp(suffix=".sqlite3"))


class ImportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.con = fresh_db()

    def test_import_then_query_matches_catalog(self) -> None:
        result = db.import_catalog(self.con, CATALOG)
        self.assertGreater(result["counts"]["capabilities"], 50)
        self.assertEqual(len(result["added"]), result["counts"]["capabilities"])
        caps = db.list_capabilities(self.con, limit=1000)
        self.assertEqual(caps["total"], result["counts"]["capabilities"])

    def test_reimport_is_idempotent_and_reports_contract_changes(self) -> None:
        db.import_catalog(self.con, CATALOG)
        again = db.import_catalog(self.con, CATALOG)
        self.assertEqual(again["added"], [])
        self.assertEqual(again["changed"], [])
        self.assertEqual(again["removed"], [])
        # 改一条的契约字段 → 只报那条“变更”
        import copy

        tampered = copy.deepcopy(CATALOG)
        for cap in tampered["capabilities"]:
            if cap["capability_id"] == "display.audio":
                cap["definition"]["typical_triggers"] = ["被改过的触发语"]
        res = db.import_catalog(self.con, tampered)
        self.assertEqual(res["changed"], ["display.audio"])
        self.assertEqual(res["added"], [])

    def test_marketplace_annotations_survive_reimport(self) -> None:
        """核心保证：集市自己维护的字段，重导入不许覆盖。"""
        db.import_catalog(self.con, CATALOG)
        db.annotate(self.con, "display.audio", {"status": "active", "owner": "gaolei", "tags": "投屏,音频",
                                                "notes": "电视出声确认过"}, actor="test")
        db.import_catalog(self.con, CATALOG)  # 再导一次
        cap = db.get_capability(self.con, "display.audio")
        self.assertEqual(cap["owner"], "gaolei")
        self.assertEqual(cap["tags"], ["投屏", "音频"])
        self.assertEqual(cap["notes"], "电视出声确认过")
        self.assertTrue(cap["reviewed_at"])
        self.assertTrue(any(e["field"] == "owner" for e in cap["events"]))

    def test_removed_capability_is_soft_deleted_and_restored(self) -> None:
        import copy

        catalog = copy.deepcopy(CATALOG)
        db.import_catalog(self.con, catalog)
        catalog["capabilities"] = [c for c in catalog["capabilities"] if c["capability_id"] != "clock.now"]
        res = db.import_catalog(self.con, catalog)
        self.assertIn("clock.now", res["removed"])
        self.assertFalse(db.get_capability(self.con, "clock.now")["in_catalog"])
        # 回不来的条目不算在目录里（默认只列 in_catalog=1）
        ids = [c["capability_id"] for c in db.list_capabilities(self.con, limit=1000)["capabilities"]]
        self.assertNotIn("clock.now", ids)
        # 代码里回来了 → 恢复（而不是新增）
        res2 = db.import_catalog(self.con, CATALOG)
        self.assertIn("clock.now", res2["restored"])
        self.assertTrue(db.get_capability(self.con, "clock.now")["in_catalog"])

    def test_search_group_and_reconcile_queries(self) -> None:
        db.import_catalog(self.con, CATALOG)
        self.assertEqual(db.list_capabilities(self.con, q="电视")["total"], 
                         sum(1 for c in CATALOG["capabilities"] if "电视" in json.dumps(c, ensure_ascii=False)))
        self.assertTrue(db.list_capabilities(self.con, q="电视 音频")["total"] >= 1)
        self.assertTrue(db.list_capabilities(self.con, q="asset_ref")["total"] >= 1)
        self.assertEqual(db.list_capabilities(self.con, group="display")["total"], 7)
        self.assertTrue(db.list_capabilities(self.con, kind="system")["total"] >= 1)
        self.assertTrue(db.list_capabilities(self.con, live="declared_not_live")["total"] >= 1)
        self.assertEqual(
            sorted(c["capability_id"] for c in db.list_capabilities(self.con, live="live_not_declared")["capabilities"]),
            ["display.audio.control", "map.route.estimate", "xiaodu.control", "xiaodu.play"],
        )
        self.assertTrue(db.list_capabilities(self.con, edge="客厅 · Mac Edge")["total"] >= 40)

    def test_annotate_validation_and_search_blob(self) -> None:
        db.import_catalog(self.con, CATALOG)
        with self.assertRaises(ValueError):
            db.annotate(self.con, "clock.now", {"status": "whatever"})
        db.annotate(self.con, "clock.now", {"owner": "gaolei", "notes": "只在整点报时用"})
        self.assertEqual(db.list_capabilities(self.con, q="整点报时")["total"], 1)
        self.assertEqual(db.list_capabilities(self.con, owner="gaolei")["total"], 1)

    def test_facets_and_export(self) -> None:
        db.import_catalog(self.con, CATALOG)
        f = db.facets(self.con)
        self.assertEqual(len(f["groups"]), len({c["group"] for c in CATALOG["capabilities"]}))
        self.assertTrue(f["edges"])
        exported = db.export_catalog(self.con)
        self.assertEqual(exported["schema"], "home-agent.capability-catalog/v1")
        self.assertEqual(exported["summary"]["capabilities"], len(CATALOG["capabilities"]))
        cap = next(c for c in exported["capabilities"] if c["capability_id"] == "display.audio")
        self.assertIn("status", cap)
        self.assertIn("owner", cap)


if __name__ == "__main__":
    unittest.main()

