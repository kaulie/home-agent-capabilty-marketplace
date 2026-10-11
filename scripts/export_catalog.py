#!/usr/bin/env python3
"""从本仓 plugins/ + declarations/ 导出能力目录。

集市是声明权威：不读 home-agent-os / brain / gateway 的 Python。
定义层来自 declarations/capabilities.json（一次性从 os 迁入后只在本仓改）；
能力包来自 plugins/*/manifest.yaml + capability.md。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_ID = "home-agent.capability-catalog/v1"
GENERATED_BY = "scripts/export_catalog.py"

DEFINITION_FIELDS = (
    "kind",
    "composition",
    "role",
    "planner_recognize",
    "typical_triggers",
    "do_not_dispatch",
    "decomposes_to",
    "prefer_when",
    "group",
    "display_name",
    "input_schema",
    "output_schema",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root()),
            capture_output=True,
            text=True,
            timeout=5,
        )
        return (out.stdout or "").strip()
    except Exception:  # noqa: BLE001
        return ""


def _blank_layer() -> dict[str, Any]:
    return {
        "kind": "",
        "composition": "atomic",
        "role": "",
        "planner_recognize": "",
        "typical_triggers": [],
        "do_not_dispatch": [],
        "decomposes_to": [],
        "prefer_when": "",
        "group": "",
        "display_name": "",
        "input_schema": {},
        "output_schema": {},
    }


def _new_entry(cid: str) -> dict[str, Any]:
    return {
        "capability_id": cid,
        "kind": "",
        "composition": "atomic",
        "role": "",
        "group": "",
        "display_name": "",
        "definition": _blank_layer(),
        "declared_by": [],
        "declared_lists": [],
        "packages": [],
        "docs": [],
        "entry": {},
        "runs_on": [],
        "config_keys": [],
        "availability": {"has_checker": False},
        "in_ads": False,
    }


def _manifest_packages(root: Path) -> list[dict[str, Any]]:
    packages: list[dict[str, Any]] = []
    plugins = root / "plugins"
    if not plugins.is_dir():
        return packages
    for manifest in sorted(plugins.glob("*/manifest.yaml")):
        text = manifest.read_text(encoding="utf-8")
        pkg: dict[str, Any] = {
            "package": manifest.parent.name,
            "docs": f"plugins/{manifest.parent.name}/capability.md",
            "capability_ids": [],
            "config_keys": [],
        }
        for key in ("id", "service_id", "group", "version", "display_name", "description"):
            m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
            if m:
                pkg[key] = m.group(1).strip().strip('"').strip("'")
        pkg["entry"] = {}
        entry_block = re.search(r"^entry:\s*\n((?:\s{2,}\S.*\n|\s*\n)*)", text, re.M)
        if entry_block:
            for m in re.finditer(r"^\s{2}([A-Za-z_][\w]*):\s*(.+)$", entry_block.group(1), re.M):
                value = m.group(2).strip().strip('"').strip("'")
                if value.endswith("/"):
                    continue
                pkg["entry"][m.group(1).strip()] = value
        pkg["platforms"] = []
        plat_block = re.search(r"^platforms:\s*\n((?:\s*-\s*\S.*\n?)+)", text, re.M)
        if plat_block:
            pkg["platforms"] = [m.group(1).strip() for m in re.finditer(r"-\s*([\w.\-]+)", plat_block.group(1))]
        caps_block = re.search(r"^capabilities:\s*\n((?:\s+.*\n|\s*\n)*)", text, re.M)
        if caps_block:
            for m in re.finditer(r"^\s+-\s*(?:capability_id:\s*)?([A-Za-z][\w.\-]*)\s*$", caps_block.group(1), re.M):
                cid = m.group(1).strip()
                if cid not in pkg["capability_ids"]:
                    pkg["capability_ids"].append(cid)
        for m in re.finditer(r"^\s+-\s+key:\s*([A-Za-z0-9_]+)", text, re.M):
            if m.group(1) not in pkg["config_keys"]:
                pkg["config_keys"].append(m.group(1))
        if (manifest.parent / "capability.md").is_file():
            pkg["docs"] = f"plugins/{manifest.parent.name}/capability.md"
        else:
            pkg["docs"] = ""
        packages.append(pkg)
    return packages


def _load_seed() -> dict[str, Any]:
    path = repo_root() / "declarations" / "capabilities.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _overlay_packages(by_id: dict[str, dict[str, Any]], packages: list[dict[str, Any]]) -> None:
    for pkg in packages:
        sid = str(pkg.get("service_id") or "").strip()
        for cid in pkg["capability_ids"]:
            e = by_id.setdefault(cid, _new_entry(cid))
            if pkg["package"] not in e["packages"]:
                e["packages"].append(pkg["package"])
            if pkg.get("docs") and pkg["docs"] not in e["docs"]:
                e["docs"].append(pkg["docs"])
            if sid and sid not in e["declared_by"]:
                e["declared_by"].append(sid)
            for host, path in (pkg.get("entry") or {}).items():
                e.setdefault("entry", {})[host] = path
                if host not in e["runs_on"]:
                    e["runs_on"].append(host)
            for host in pkg.get("platforms") or []:
                if host not in e["runs_on"]:
                    e["runs_on"].append(host)
            for key in pkg.get("config_keys") or []:
                if key not in e["config_keys"]:
                    e["config_keys"].append(key)
            definition = e.setdefault("definition", _blank_layer())
            if pkg.get("group") and not definition.get("group"):
                definition["group"] = pkg["group"]
            if pkg.get("display_name") and not definition.get("display_name"):
                definition["display_name"] = pkg["display_name"]
            sources = definition.setdefault("sources", [])
            tag = f"package:{pkg['package']}"
            if tag not in sources:
                sources.append(tag)


def _finish_entries(by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    capabilities: list[dict[str, Any]] = []
    for e in by_id.values():
        for field in ("declared_by", "declared_lists", "packages", "docs", "config_keys", "runs_on"):
            e[field] = sorted(dict.fromkeys(e.get(field) or []))
        definition = e.setdefault("definition", _blank_layer())
        for field in ("typical_triggers", "do_not_dispatch", "decomposes_to"):
            if definition.get(field):
                definition[field] = sorted(dict.fromkeys(definition[field]))
        if definition.get("sources"):
            definition["sources"] = sorted(dict.fromkeys(definition["sources"]))
        for field, fallback in (
            ("kind", ""),
            ("composition", "atomic"),
            ("role", ""),
            ("group", ""),
            ("display_name", ""),
        ):
            e[field] = str(definition.get(field) or fallback)
        if not e["group"]:
            cid = e["capability_id"]
            e["group"] = cid.split(".", 1)[0] if "." in cid else "(未分类)"
        capabilities.append(e)
    capabilities.sort(key=lambda x: x["capability_id"])
    return capabilities


def build_catalog() -> dict[str, Any]:
    seed = _load_seed()
    packages = _manifest_packages(repo_root())
    by_id: dict[str, dict[str, Any]] = {}
    for cap in seed.get("capabilities") or []:
        cid = str(cap.get("capability_id") or "").strip()
        if cid:
            by_id[cid] = json.loads(json.dumps(cap))
    _overlay_packages(by_id, packages)
    capabilities = _finish_entries(by_id)

    services = list(seed.get("services") or [])
    known = {str(s.get("service_id") or "") for s in services}
    for pkg in packages:
        sid = str(pkg.get("service_id") or "").strip()
        if not sid or sid in known:
            continue
        services.append(
            {
                "constant": "",
                "service_id": sid,
                "display_name": str(pkg.get("display_name") or ""),
                "group": str(pkg.get("group") or ""),
                "version": str(pkg.get("version") or ""),
                "capabilities": list(pkg.get("capability_ids") or []),
                "source": "plugin",
            }
        )
        known.add(sid)

    groups: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for e in capabilities:
        groups[e["group"] or "(未分类)"] = groups.get(e["group"] or "(未分类)", 0) + 1
        kinds[e["kind"] or "(未标注)"] = kinds.get(e["kind"] or "(未标注)", 0) + 1

    seed_summary = seed.get("summary") or {}
    return {
        "schema": SCHEMA_ID,
        "generated_by": GENERATED_BY,
        "generated_at": _now_iso(),
        "source": {
            "repo": "home-agent-capabilty-marketplace",
            "commit": _git_commit(),
            "edge": "marketplace",
        },
        "summary": {
            "capabilities": len(capabilities),
            "ads_definitions": int(seed_summary.get("ads_definitions") or 0),
            "declared_capabilities": sum(len(s.get("capabilities") or []) for s in services),
            "services": len(services),
            "extensions": len(packages),
            "with_checker": sum(1 for e in capabilities if (e.get("availability") or {}).get("has_checker")),
            "brain_wire": int(seed_summary.get("brain_wire") or 0),
            "groups": dict(sorted(groups.items())),
            "kinds": dict(sorted(kinds.items())),
        },
        "services": sorted(services, key=lambda s: str(s.get("service_id") or "")),
        "capabilities": capabilities,
    }


def catalog_schema() -> dict[str, Any]:
    existing = repo_root() / "schema" / "catalog.schema.json"
    if existing.is_file():
        return json.loads(existing.read_text(encoding="utf-8"))
    return {"$id": SCHEMA_ID}


def _md_escape(text: Any) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ").strip()


def _param_rows(schema: dict[str, Any]) -> list[str]:
    rows: list[str] = []
    for name in sorted(schema or {}):
        spec = schema.get(name) or {}
        if not isinstance(spec, dict):
            continue
        req = "是" if spec.get("required") else "否"
        rows.append(
            f"| `{name}` | {_md_escape(spec.get('type') or '')} | {req} | {_md_escape(spec.get('description'))} |"
        )
    return rows


def effective_view(cap: dict[str, Any]) -> dict[str, Any]:
    view: dict[str, Any] = {}
    definition = cap.get("definition") or {}
    for field in DEFINITION_FIELDS:
        value = definition.get(field)
        view[field] = value if value is not None else ([] if field.endswith("s") and field != "prefer_when" else "")
    view["sources"] = definition.get("sources") or []
    return view


def render_capability_md(cap: dict[str, Any], catalog: dict[str, Any]) -> str:
    cid = cap["capability_id"]
    view = effective_view(cap)
    lines: list[str] = [f"# `{cid}`", ""]
    headline = " · ".join(x for x in (view.get("display_name"), view.get("role")) if x)
    if headline:
        lines += [headline, ""]
    flags = [
        f"kind=`{view.get('kind') or '-'}`",
        f"composition=`{view.get('composition') or '-'}`",
        f"group=`{view.get('group') or '-'}`",
        f"声明=`{'是' if cap.get('in_ads') or cap.get('declared_by') or cap.get('declared_lists') else '否'}`",
        f"执行前自检=`{'有' if cap.get('availability', {}).get('has_checker') else '无'}`",
    ]
    lines += [" · ".join(flags), ""]
    if view.get("planner_recognize"):
        lines += ["## 规划器怎么认它", "", view["planner_recognize"], ""]
    if view.get("prefer_when"):
        lines += [f"> 优先本能力：{view['prefer_when']}", ""]
    if view.get("typical_triggers"):
        lines += ["## 典型触发语", ""] + [f"- {t}" for t in view["typical_triggers"]] + [""]
    if view.get("do_not_dispatch"):
        lines += ["## 不要派给它", ""] + [f"- {t}" for t in view["do_not_dispatch"]] + [""]
    rows = _param_rows(view.get("input_schema") or {})
    lines += ["## 入参", ""]
    lines += (["| 参数 | 类型 | 必填 | 说明 |", "|---|---|---|---|"] + rows) if rows else ["（无）"]
    lines += [""]
    out_rows = _param_rows(view.get("output_schema") or {})
    lines += ["## 出参", ""]
    lines += (["| 参数 | 类型 | 必填 | 说明 |", "|---|---|---|---|"] + out_rows) if out_rows else ["（无）"]
    lines += [""]
    if cap.get("runs_on"):
        lines += ["## 适用宿主（代码事实）", ""] + [f"- `{h}`" for h in cap["runs_on"]] + [""]
    if cap.get("declared_by"):
        lines += ["## 服务声明", ""] + [f"- `{s}`" for s in cap["declared_by"]] + [""]
    if cap.get("packages"):
        lines += ["## 能力包", ""] + [f"- `plugins/{p}/`" for p in cap["packages"]] + [""]
    if cap.get("docs"):
        lines += ["## 文档", ""]
        for d in cap["docs"]:
            lines.append(f"- [{d}](../{d})")
        lines += [""]
    if cap.get("entry"):
        lines += ["## 入口", ""]
        for platform, path in sorted(cap["entry"].items()):
            lines.append(f"- {platform}: `{path}`")
        lines += [""]
    lines += [
        "",
        "---",
        "",
        f"<sub>由 `{catalog.get('generated_by')}` 生成（marketplace `{catalog.get('source', {}).get('commit')}`），请勿手改。</sub>",
        "",
    ]
    return "\n".join(lines)


def render_catalog_md(catalog: dict[str, Any]) -> str:
    s = catalog["summary"]
    src = catalog["source"]
    caps = catalog["capabilities"]
    lines: list[str] = [
        "# 能力总表",
        "",
        f"> 由 `{catalog['generated_by']}` 从本仓 `plugins/` + `declarations/` 生成"
        f"（{catalog['generated_at']}，commit `{src.get('commit') or '-'}`）；**请勿手改**。"
        " 改声明请改本仓再跑 `scripts/sync.sh`。",
        "",
        "## 概览",
        "",
        "| 项 | 数 |",
        "|---|---|",
        f"| 能力总数 | {s['capabilities']} |",
        f"| 服务 | {s['services']} |",
        f"| 能力包（plugins/*/manifest.yaml） | {s['extensions']} |",
        "",
        "### 按 group",
        "",
        "| group | 能力数 |",
        "|---|---|",
    ]
    for group, count in sorted(s["groups"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| `{group}` | {count} |")
    lines += ["", "## 能力清单（按 group）", ""]
    by_group: dict[str, list[dict[str, Any]]] = {}
    for cap in caps:
        by_group.setdefault(cap.get("group") or "(未分类)", []).append(cap)
    for group in sorted(by_group):
        lines += [f"### `{group}`", "", "| 能力 | kind | 角色 | 触发语（示例） |", "|---|---|---|---|"]
        for cap in by_group[group]:
            role = cap.get("role") or cap.get("display_name") or ""
            trigger = ((cap.get("definition") or {}).get("typical_triggers") or [""])[0]
            lines.append(
                f"| [`{cap['capability_id']}`](capabilities/{cap['capability_id']}.md) | {cap.get('kind') or '-'} | "
                f"{_md_escape(role)} | {_md_escape(trigger)} |"
            )
        lines += [""]
    lines += ["", "---", "", f"`{catalog['schema']}`", ""]
    return "\n".join(lines)


def _dump(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def write_catalog(catalog: dict[str, Any], out: Path) -> list[str]:
    out = Path(out)
    (out / "catalog").mkdir(parents=True, exist_ok=True)
    (out / "capabilities").mkdir(parents=True, exist_ok=True)
    (out / "schema").mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    files = {
        "catalog/capabilities.json": _dump(catalog),
        "catalog/capabilities.md": render_catalog_md(catalog) + "\n",
        "schema/catalog.schema.json": _dump(catalog_schema()),
    }
    for rel, text in files.items():
        (out / rel).write_text(text, encoding="utf-8")
        written.append(rel)
    wanted: set[str] = set()
    for cap in catalog["capabilities"]:
        rel = f"capabilities/{cap['capability_id']}.md"
        (out / rel).write_text(render_capability_md(cap, catalog), encoding="utf-8")
        wanted.add(rel)
        written.append(rel)
    for old in (out / "capabilities").glob("*.md"):
        rel = f"capabilities/{old.name}"
        if rel not in wanted:
            old.unlink()
            written.append(f"-{rel}")
    return sorted(written)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="从本仓声明导出能力目录")
    parser.add_argument("--out", required=True, help="目标目录")
    args = parser.parse_args(argv)
    catalog = build_catalog()
    written = write_catalog(catalog, Path(args.out))
    s = catalog["summary"]
    print(
        f"[ok] 写 {len(written)} 个文件 → {args.out}\n"
        f"     能力 {s['capabilities']} / 服务 {s['services']} / 能力包 {s['extensions']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
