#!/usr/bin/env python3
"""本仓导出器：不读 os/brain/gateway，xiaodu.play 与 xiaodu.speaker 是两个插件。"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_catalog.py"
_spec = importlib.util.spec_from_file_location("export_catalog", EXPORTER)
assert _spec and _spec.loader
exporter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exporter)


class ExportCatalogTest(unittest.TestCase):
    def test_source_is_marketplace(self) -> None:
        catalog = exporter.build_catalog()
        self.assertEqual(catalog["source"]["repo"], "home-agent-capabilty-marketplace")
        self.assertEqual(catalog["source"]["edge"], "marketplace")
        self.assertEqual(catalog["generated_by"], "scripts/export_catalog.py")

    def test_xiaodu_play_is_independent_plugin(self) -> None:
        catalog = exporter.build_catalog()
        by_id = {c["capability_id"]: c for c in catalog["capabilities"]}
        play = by_id["xiaodu.play"]
        speak = by_id["xiaodu.speak"]
        self.assertIn("xiaodu-play", play["packages"])
        self.assertIn("xiaodu-speaker", speak["packages"])
        self.assertNotIn("xiaodu-speaker", play["packages"])
        self.assertIn("xiaodu.play", play["declared_by"])
        self.assertIn("xiaodu.speaker", speak["declared_by"])
        self.assertNotIn("xiaodu.speaker", play["declared_by"])

    def test_decomposes_to_keeps_execution_order(self) -> None:
        catalog = exporter.build_catalog()
        by_id = {c["capability_id"]: c for c in catalog["capabilities"]}
        composite = by_id["camera.capture_and_upload"]
        parts = (composite.get("definition") or {}).get("decomposes_to") or composite.get(
            "decomposes_to"
        )
        self.assertEqual(parts, ["camera.capture", "asset.upload"])

    def test_write_pages(self) -> None:
        catalog = exporter.build_catalog()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            exporter.write_catalog(catalog, out)
            self.assertTrue((out / "capabilities/xiaodu.play.md").is_file())
            md = (out / "capabilities/xiaodu.play.md").read_text(encoding="utf-8")
            self.assertIn("plugins/xiaodu-play/", md)
            self.assertNotIn("home-agent-os", md)


if __name__ == "__main__":
    unittest.main()
