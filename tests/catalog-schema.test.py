#!/usr/bin/env python3
"""catalog 结构校验（只用标准库）：目录自身的一致性（**声明视图**）。

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
# 集市定位：能力展示与技能介绍（静态声明）；这些实时概念一律不该出现在目录/导出里
FORBIDDEN = ("in_live", "live", "providers", "reconcile")

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        FAILURES.append(msg)


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    caps = catalog["capabilities"]
    current = [c for c in caps if c.get("in_catalog")]  # 软删条目仍在库（留注解/历史），不算当前目录
    summary = catalog["summary"]

    check(catalog["schema"] == SCHEMA_ID, "catalog.schema 不是 " + SCHEMA_ID)
    check(catalog.get("kind") == "declaration", "catalog.kind 应为 declaration（集市只登记声明）")
    check(schema["$id"] == SCHEMA_ID, "schema/$id 与 catalog 不一致")
    check(len({c["capability_id"] for c in caps}) == len(caps), "capability_id 有重复")

    for cap in current:
        cid = cap["capability_id"]
        check(bool(cap.get("kind")), f"{cid}: 缺 kind")
        check(bool(cap.get("composition")), f"{cid}: 缺 composition")
        check(bool(cap.get("group")), f"{cid}: 缺 group（UI 分组会漏）")
        check("definition" in cap, f"{cid}: 缺 definition 层")
        check("declaration" in cap, f"{cid}: 缺 declaration 块")
        decl = cap.get("declaration") or {}
        for key in ("in_ads", "declared_by", "conditional_lists", "packages", "has_preflight"):
            check(key in decl, f"{cid}: declaration 缺 {key}")
        for market_field in ("status", "owner", "tags", "notes", "hosts", "in_catalog"):
            check(market_field in cap, f"{cid}: 缺集市字段 {market_field}")
        for host_field in ("runs_on", "hosts_effective"):
            check(isinstance(cap.get(host_field), list), f"{cid}: {host_field} 必须是数组")
        check(cap.get("hosts_source") in ("curated", "code", "none"), f"{cid}: hosts_source 取值非法")
        for gone in FORBIDDEN:
            check(gone not in cap, f"{cid}: 不该出现实时字段 {gone}")

    check(summary["capabilities"] == len(current), "summary.capabilities 与条目数不一致")
    groups: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for cap in current:
        groups[cap["group"]] = groups.get(cap["group"], 0) + 1
        kinds[cap["kind"] or "(未标注)"] = kinds.get(cap["kind"] or "(未标注)", 0) + 1
    check(groups == summary["groups"], "summary.groups 与条目不一致")
    check(kinds == summary["kinds"], "summary.kinds 与条目不一致")

    host_ids = {h.get("host_id") for h in catalog.get("hosts") or []}
    check(bool(host_ids), "catalog.hosts（宿主注册表）不该为空")
    for cap in current:
        for host in cap.get("hosts_effective") or []:
            check(host in host_ids, f"{cap['capability_id']}: 宿主 {host} 不在注册表里")

    pages = {p.stem for p in (ROOT / "capabilities").glob("*.md")}
    check(pages == {c["capability_id"] for c in current}, "capabilities/*.md 与能力集合不一致")

    for rel in (
        "index.html", "web/index.html", "web/assets/app.js", "web/assets/catalog-core.js",
        "web/assets/styles.css", "catalog/capabilities.md", "server/marketplace.py", "server/catalog_cli.py",
    ):
        check((ROOT / rel).is_file(), f"缺少 {rel}")

    if FAILURES:
        print(f"[catalog] {len(FAILURES)} 处不自洽：", file=sys.stderr)
        for f in FAILURES[:30]:
            print("  -", f, file=sys.stderr)
        return 1
    print(f"[catalog] OK：{len(current)} 条能力声明（另有 {len(caps) - len(current)} 条已下线留档）/ {len(groups)} 组 / "
          f"服务归属 {summary['with_service']} / 条件挂载 {summary['conditional']} / 适用宿主 {summary.get('with_hosts')}（宿主 {len(host_ids)} 个）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
