#!/usr/bin/env python3
"""catalog-drift：比对「代码重新导出的目录」与「仓库里的目录」的**契约字段**。

用法：python3 tests/catalog-drift.py <新导出.json> <仓库里的 catalog.json>

只比**声明字段**（能力增删 + 契约字段）：集市注解（status/owner/tags/notes）是集市自己维护的；
代码里已下线而库里留档的条目（in_catalog=0，软删）也不算漂移。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIELDS = (
    "kind", "composition", "group", "display_name", "role", "planner_recognize",
    "typical_triggers", "do_not_dispatch", "input_schema", "output_schema", "in_ads",
)


def view(catalog: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for cap in catalog.get("capabilities") or []:
        if not cap.get("in_catalog", 1):
            continue  # 软删留档（代码里已下线）：不算漂移
        definition = cap.get("definition") or {}
        row = {k: definition.get(k, cap.get(k)) for k in FIELDS}
        out[cap["capability_id"]] = row
    return out


def drift(new_catalog: dict, repo_catalog: dict) -> list[str]:
    a, b = view(new_catalog), view(repo_catalog)
    problems: list[str] = []
    for cid in sorted(set(a) - set(b)):
        problems.append(f"代码里有、仓库里没有：{cid}")
    for cid in sorted(set(b) - set(a)):
        problems.append(f"仓库里有、代码里没了：{cid}")
    for cid in sorted(set(a) & set(b)):
        if a[cid] != b[cid]:
            diff = [k for k in FIELDS if a[cid].get(k) != b[cid].get(k)]
            problems.append(f"{cid} 契约字段变了：{', '.join(diff)}")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    new_catalog = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    repo_catalog = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    problems = drift(new_catalog, repo_catalog)
    if problems:
        print(f"[drift] {len(problems)} 处漂移（跑一次不带 --check 的 sync 修正）：", file=sys.stderr)
        for p in problems[:40]:
            print("  -", p, file=sys.stderr)
        return 1
    print("[drift] 一致 ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
