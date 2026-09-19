#!/usr/bin/env python3
"""catalog 结构校验（只用标准库）：这个仓库自己的一致性，不依赖 home-agent-os。

校验「目录本身是不是自洽」：schema 对得上、每页 md 都在、计数与内容一致、账不平标记自洽。
跑法：python3 tests/catalog-schema.test.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "capabilities.json"
SCHEMA = ROOT / "schema" / "catalog.schema.json"
SCHEMA_ID = "home-agent.capability-catalog/v1"

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        FAILURES.append(msg)


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    caps = catalog["capabilities"]
    summary = catalog["summary"]

    check(catalog["schema"] == SCHEMA_ID, "catalog.schema 不是 " + SCHEMA_ID)
    check(schema["$id"] == SCHEMA_ID, "schema/$id 与 catalog 不一致")
    check(all(c.get("capability_id") for c in caps), "有缺少 capability_id 的条目")
    check(len({c["capability_id"] for c in caps}) == len(caps), "capability_id 有重复")

    for cap in caps:
        cid = cap["capability_id"]
        check(bool(cap.get("kind")), f"{cid}: 缺 kind")
        check(bool(cap.get("composition")), f"{cid}: 缺 composition")
        check(bool(cap.get("group")), f"{cid}: 缺 group（UI 分组会漏）")
        check("definition" in cap, f"{cid}: 缺 definition 层")
        # 集市字段（DB 拥有的那几列）必须在导出里可见 —— 否则静态 UI 看不到「谁维护过」
        for market_field in ("status", "owner", "tags", "notes", "in_catalog"):
            check(market_field in cap, f"{cid}: 缺集市字段 {market_field}")
        rec = cap.get("reconcile") or {}
        check(
            rec.get("declared_not_live")
            == bool((cap.get("in_ads") or cap.get("declared_by") or cap.get("declared_lists")) and not cap.get("in_live")),
            f"{cid}: declared_not_live 标记与 in_ads/in_live 不自洽",
        )
        check(rec.get("live_not_declared") == bool(cap.get("in_live") and not cap.get("in_ads")), f"{cid}: live_not_declared 不自洽")

    # 计数与内容一致（账不平两个数由 UI 直接展示，必须真）
    check(summary["capabilities"] == len(caps), "summary.capabilities 与条目数不一致")
    check(
        summary["declared_not_live"] == sum(1 for c in caps if c["reconcile"]["declared_not_live"]),
        "summary.declared_not_live 与条目不一致",
    )
    check(
        summary["live_not_declared"] == sum(1 for c in caps if c["reconcile"]["live_not_declared"]),
        "summary.live_not_declared 与条目不一致",
    )
    # groups/kinds 汇总
    groups: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for cap in caps:
        groups[cap["group"]] = groups.get(cap["group"], 0) + 1
        kinds[cap["kind"] or "(未标注)"] = kinds.get(cap["kind"] or "(未标注)", 0) + 1
    check(groups == summary["groups"], "summary.groups 与条目不一致")
    check(kinds == summary["kinds"], "summary.kinds 与条目不一致")

    # 每个能力一页，且没有多余页面
    pages = {p.stem for p in (ROOT / "capabilities").glob("*.md")}
    check(pages == {c["capability_id"] for c in caps}, "capabilities/*.md 与能力集合不一致")

    # UI 的必需资源在
    for rel in (
        "index.html",
        "web/index.html",
        "web/assets/app.js",
        "web/assets/catalog-core.js",
        "web/assets/styles.css",
        "catalog/capabilities.md",
        "server/marketplace.py",
        "server/catalog_cli.py",
    ):
        check((ROOT / rel).is_file(), f"缺少 {rel}")

    if FAILURES:
        print(f"[catalog] {len(FAILURES)} 处不自洽：", file=sys.stderr)
        for f in FAILURES[:30]:
            print("  -", f, file=sys.stderr)
        return 1
    print(f"[catalog] OK：{len(caps)} 条能力 / {len(groups)} 组 / 在线 {summary['live']} / 声明未上线 {summary['declared_not_live']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
