#!/usr/bin/env python3
"""catalog_cli.py：能力集市数据库的命令行入口（导入 / 导出 / 统计 / 注解 / 起服务）。

    python3 server/catalog_cli.py import  catalog/capabilities.json --note "sync from home-agent-os"
    python3 server/catalog_cli.py export  --out catalog/capabilities.json     # DB → JSON（含注解）
    python3 server/catalog_cli.py stats
    python3 server/catalog_cli.py annotate display.audio --status active --owner gaolei --tags 投屏,音频 --notes "电视出声确认过"
    python3 server/catalog_cli.py serve --port 4250

DB 路径：`--db` > `$MARKETPLACE_DB` > `<repo>/data/marketplace.sqlite3`
（生产用 `~/database/home-agent-capability-marketplace/marketplace.sqlite3`，见 scripts/start.sh）。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import db  # noqa: E402


def default_db() -> str:
    return os.environ.get("MARKETPLACE_DB") or str(REPO / "data" / "marketplace.sqlite3")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="能力集市数据库工具")
    p.add_argument("--db", default=default_db(), help="SQLite 路径")
    sub = p.add_subparsers(dest="cmd", required=True)

    imp = sub.add_parser("import", help="导入导出器的 catalog JSON")
    imp.add_argument("file", help="catalog JSON 路径（'-' = stdin）")
    imp.add_argument("--note", default="", help="这次导入的备注（记进 imports 表）")

    exp = sub.add_parser("export", help="DB → catalog JSON（含集市注解）")
    exp.add_argument("--out", default=str(REPO / "catalog" / "capabilities.json"))

    sub.add_parser("stats", help="库概览")

    ann = sub.add_parser("annotate", help="改集市自有字段（status/owner/tags/notes）")
    ann.add_argument("capability_id")
    ann.add_argument("--status", choices=list(db.VALID_STATUS))
    ann.add_argument("--owner", default=None)
    ann.add_argument("--tags", default=None, help="逗号分隔")
    ann.add_argument("--notes", default=None)
    ann.add_argument("--actor", default="cli")

    srv = sub.add_parser("serve", help="起 HTTP 服务（API + UI）")
    srv.add_argument("--host", default=os.environ.get("MARKETPLACE_HOST", "0.0.0.0"))
    srv.add_argument("--port", type=int, default=int(os.environ.get("MARKETPLACE_PORT", "4250")))
    srv.add_argument("--web", default=str(REPO / "web"), help="UI 静态目录")
    srv.add_argument("--static", default=str(REPO), help="仓库根（catalog/ capabilities/ schema/ 静态）")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if args.cmd == "serve":
        import marketplace  # noqa: PLC0415  （只有起服务时才需要）

        marketplace.serve(
            db_path=args.db, host=args.host, port=args.port, web_dir=Path(args.web), static_dir=Path(args.static)
        )
        return 0

    con = db.connect(args.db)
    try:
        return _dispatch(args, con)
    finally:
        con.close()  # 一次性命令用完就关：否则解释器退出时报 ResourceWarning: unclosed database


def _dispatch(args: argparse.Namespace, con: "db.sqlite3.Connection") -> int:
    if args.cmd == "import":
        raw = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
        catalog = json.loads(raw)
        result = db.import_catalog(con, catalog, note=args.note)
        print(
            f"[import] #{result['import_id']} 能力 {result['counts']['capabilities']} 条"
            f"（新增 {len(result['added'])} / 变更 {len(result['changed'])} / "
            f"下线 {len(result['removed'])} / 恢复 {len(result['restored'])} / "
            f"保留注解 {len(result['preserved'])}）"
        )
        for cid in result["removed"][:10]:
            print(f"  - 下线：{cid}")
        for cid in result["changed"][:10]:
            print(f"  ~ 契约变更：{cid}")
        return 0

    if args.cmd == "export":
        catalog = db.export_catalog(con)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        s = catalog["summary"]
        print(f"[export] {out} 能力 {s['capabilities']}（有服务归属 {s['with_service']} / 条件挂载 {s['conditional']} / 已策展 {s['annotated']}）")
        return 0

    if args.cmd == "stats":
        s = db.stats(con)
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "annotate":
        fields: dict[str, object] = {}
        for key in ("status", "owner", "tags", "notes"):
            value = getattr(args, key)
            if value is not None:
                fields[key] = value
        try:
            cap = db.annotate(con, args.capability_id, fields, actor=args.actor)
        except ValueError as e:
            print(f"[annotate][错误] {e}", file=sys.stderr)
            return 2
        if cap is None:
            print(f"[annotate][错误] 找不到 {args.capability_id}", file=sys.stderr)
            return 1
        print(
            f"[annotate] {cap['capability_id']} status={cap['status']} owner={cap['owner']} "
            f"tags={cap['tags']} reviewed_at={cap['reviewed_at']}"
        )
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
