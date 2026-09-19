"""db.py：能力集市的**独立数据库**（SQLite）。

为什么要库而不是只留生成好的 JSON：
- **集市自有字段**（status/owner/tags/notes/评审）要能自己管，而且**重导入不能覆盖**；
- 查询要能按关键字/group/kind/设备/状态**服务端**过滤（数据源是库，不是文件）；
- 每次导入留痕：谁在什么时候把哪一版代码导进来、增删了什么。

导入时字段泾渭分明：
- **生成物字段**（kind/role/触发语/schema/…）：导出器给，导入即覆盖；
- **集市字段**（status/owner/tags/notes/reviewed_at）：只由人与 API 改，导入**永不覆盖**。

搜索用 `search_blob` + LIKE 子串：实测 FTS5 的 trigram 分词对 2 字中文词（「电视」）不命中，
而 `LIKE '%词%'` 对任意长度中文都正确；几百到几千条数据下全表扫描是微秒级，够用。
"""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 1
MARKETPLACE_FIELDS = ("status", "owner", "tags", "notes", "reviewed_at")
VALID_STATUS = ("active", "planned", "deprecated", "blocked")

SCHEMA_SQL = """
create table if not exists meta (key text primary key, value text not null);

create table if not exists capabilities (
  capability_id text primary key, kind text not null default '',
  composition text not null default 'atomic', group_id text not null default '',
  display_name text not null default '', role text not null default '',
  planner_recognize text not null default '', prefer_when text not null default '',
  typical_triggers text not null default '[]', do_not_dispatch text not null default '[]',
  decomposes_to text not null default '[]', input_schema text not null default '{}',
  output_schema text not null default '{}', definition_sources text not null default '[]',
  has_checker integer not null default 0, in_ads integer not null default 0,
  -- 集市自有字段（导入不覆盖）
  status text not null default 'active', owner text not null default '',
  tags text not null default '[]', notes text not null default '',
  reviewed_at text not null default '', updated_at text not null default '',
  in_catalog integer not null default 1,
  search_blob text not null default ''
);

create table if not exists live (
  capability_id text not null, edge_id text not null default '',
  edge_name text not null default '', assigned_edge_id text not null default '',
  service_id text not null default '', kind text not null default '',
  role text not null default '', planner_recognize text not null default '',
  observed_at text not null default '',
  primary key (capability_id, edge_id, service_id)
);

create table if not exists services (
  service_id text primary key, display_name text not null default '',
  group_id text not null default '', version text not null default '',
  constant text not null default '', updated_at text not null default ''
);

create table if not exists service_capabilities (
  service_id text not null, capability_id text not null,
  primary key (service_id, capability_id)
);

create table if not exists declared_lists (
  capability_id text not null, list_name text not null,
  primary key (capability_id, list_name)
);

create table if not exists packages (
  package text primary key, service_id text not null default '',
  group_id text not null default '', display_name text not null default '',
  entry_mac text not null default '', docs text not null default '',
  config_keys text not null default '[]', updated_at text not null default ''
);

create table if not exists capability_packages (
  capability_id text not null, package text not null,
  primary key (capability_id, package)
);

create table if not exists imports (
  import_id integer primary key autoincrement, imported_at text not null,
  source_repo text not null default '', source_commit text not null default '',
  live_source text not null default '', live_count integer not null default 0,
  generated_at text not null default '', caps_count integer not null default 0,
  added text not null default '[]', removed text not null default '[]',
  changed text not null default '[]', preserved text not null default '[]',
  note text not null default ''
);

create table if not exists events (
  event_id integer primary key autoincrement, at text not null,
  capability_id text not null default '', field text not null default '',
  old_value text not null default '', new_value text not null default '',
  actor text not null default 'api'
);

create index if not exists idx_caps_group on capabilities(group_id);
create index if not exists idx_caps_status on capabilities(status);
create index if not exists idx_live_cap on live(capability_id);
create index if not exists idx_pkg_cap on capability_packages(capability_id);
"""


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def connect(db_path: str | Path) -> sqlite3.Connection:
    """打开（并初始化）数据库。WAL；目录不存在会创建。"""
    path = Path(db_path)
    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(path), timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("pragma journal_mode=WAL")
    con.execute("pragma synchronous=NORMAL")
    con.executescript(SCHEMA_SQL)
    con.execute(
        "insert into meta(key, value) values('schema_version', ?) "
        "on conflict(key) do update set value=excluded.value",
        (str(SCHEMA_VERSION),),
    )
    con.commit()
    return con


def _json_list(value: Any) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(x) for x in value if str(x).strip()]
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(x) for x in parsed if str(x).strip()]
        except Exception:  # noqa: BLE001
            return []
    return []


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _loads(raw: Any, default: Any) -> Any:
    if raw in (None, ""):
        return default
    try:
        return json.loads(raw)
    except Exception:  # noqa: BLE001
        return default


def build_search_blob(row: dict[str, Any], *, extra: Iterable[str] = ()) -> str:
    """把一条能力摊平成可搜索文本（与 UI 的关键字语义一致）。"""
    parts: list[str] = [
        str(row.get("capability_id") or ""),
        str(row.get("display_name") or ""),
        str(row.get("role") or ""),
        str(row.get("group_id") or ""),
        str(row.get("kind") or ""),
        str(row.get("planner_recognize") or ""),
        str(row.get("prefer_when") or ""),
        str(row.get("owner") or ""),
        str(row.get("notes") or ""),
    ]
    for key in ("typical_triggers", "do_not_dispatch", "decomposes_to", "definition_sources", "tags"):
        parts.extend(_json_list(row.get(key)))
    for key in ("input_schema", "output_schema"):
        schema = row.get(key) or {}
        if isinstance(schema, dict):
            for name, spec in schema.items():
                parts.append(str(name))
                if isinstance(spec, dict):
                    parts.append(str(spec.get("type") or ""))
                    parts.append(str(spec.get("description") or ""))
        elif isinstance(schema, str) and schema.strip():
            parts.append(schema)
    parts.extend(str(x) for x in extra)
    return "  ".join(p for p in parts if p).lower()


GENERATOR_FIELDS = (
    "kind", "composition", "group_id", "display_name", "role", "planner_recognize",
    "prefer_when", "typical_triggers", "do_not_dispatch", "decomposes_to",
    "input_schema", "output_schema", "definition_sources", "has_checker", "in_ads",
)


def _contract_fingerprint(row: dict[str, Any]) -> str:
    """生成物字段的指纹：用来判断「代码里的契约变了」。"""
    return json.dumps({k: row.get(k) for k in GENERATOR_FIELDS}, ensure_ascii=False, sort_keys=True)


def _live_entries(cap: dict[str, Any]) -> list[dict[str, Any]]:
    """从两种 catalog 形状里取线上实况（导出器版：live={providers:[…]}；库导出：live=[行…]）。"""
    live = cap.get("live")
    if isinstance(live, dict):
        return [dict(p) for p in (live.get("providers") or []) if isinstance(p, dict)]
    if isinstance(live, list):
        return [dict(r) for r in live if isinstance(r, dict)]
    return []


def _live_contract(cap: dict[str, Any]) -> dict[str, Any]:
    """实况层的契约字段（导出器版的 live 直接带 kind/role/…；库导出放在每行里）。"""
    live = cap.get("live")
    if isinstance(live, dict):
        return dict(live)
    rows = _live_entries(cap)
    return rows[0] if rows else {}


def _pkg_hints(cap: dict[str, Any]) -> list[str]:
    """额外参与搜索的文本：服务/包/配置键/声明列表/设备名。"""
    out: list[str] = []
    for key in ("declared_by", "declared_lists", "packages", "docs", "config_keys", "registered_ids"):
        out.extend(str(x) for x in (cap.get(key) or []))
    for prov in _live_entries(cap):
        out.extend(
            [str(prov.get("edge_name") or ""), str(prov.get("service_id") or ""), str(prov.get("edge_id") or "")]
        )
    return out


def _cap_row(cap: dict[str, Any], *, now: str, extra: Iterable[str] = ()) -> dict[str, Any]:
    """把 catalog 里的一条能力摊平成 DB 行（生成物字段）。"""
    definition = cap.get("definition") or {}
    live = _live_contract(cap)
    row: dict[str, Any] = {
        "capability_id": str(cap.get("capability_id") or "").strip(),
        "kind": str(cap.get("kind") or definition.get("kind") or ""),
        "composition": str(cap.get("composition") or definition.get("composition") or "atomic"),
        "group_id": str(cap.get("group") or definition.get("group") or ""),
        "display_name": str(cap.get("display_name") or definition.get("display_name") or ""),
        "role": str(cap.get("role") or definition.get("role") or ""),
        "planner_recognize": str(definition.get("planner_recognize") or live.get("planner_recognize") or ""),
        "prefer_when": str(definition.get("prefer_when") or ""),
        "typical_triggers": _dumps(definition.get("typical_triggers") or live.get("typical_triggers") or []),
        "do_not_dispatch": _dumps(definition.get("do_not_dispatch") or live.get("do_not_dispatch") or []),
        "decomposes_to": _dumps(definition.get("decomposes_to") or []),
        "input_schema": _dumps(definition.get("input_schema") or live.get("input_schema") or {}),
        "output_schema": _dumps(definition.get("output_schema") or live.get("output_schema") or {}),
        "definition_sources": _dumps(definition.get("sources") or []),
        "has_checker": int(bool((cap.get("availability") or {}).get("has_checker"))),
        "in_ads": int(bool(cap.get("in_ads"))),
        "updated_at": now,
    }
    row["search_blob"] = build_search_blob(row, extra=extra)
    return row


def import_catalog(con: sqlite3.Connection, catalog: dict[str, Any], *, note: str = "") -> dict[str, Any]:
    """导入导出器的 catalog：**覆盖生成物字段、保留集市字段**，并留一次导入记录。

    - `removed`：代码里没了 → **软删**（in_catalog=0；集市字段/注解/历史都留着，再回来即恢复）；
    - `preserved`：这次导入明确**没有动**的集市字段（有人维护过的条目）。
    """
    now = now_iso()
    incoming: dict[str, dict[str, Any]] = {}
    for cap in catalog.get("capabilities") or []:
        cid = str(cap.get("capability_id") or "").strip()
        if cid:
            incoming[cid] = _cap_row(cap, now=now, extra=_pkg_hints(cap))

    cols = "select capability_id, in_catalog, status, owner, tags, notes, " + ", ".join(GENERATOR_FIELDS) + " from capabilities"
    existing = {r["capability_id"]: dict(r) for r in con.execute(cols)}
    added: list[str] = []
    changed: list[str] = []
    removed: list[str] = []
    restored: list[str] = []
    preserved: list[str] = []

    for cid, row in incoming.items():
        prev = existing.get(cid)
        if prev is None:
            con.execute(
                "insert into capabilities (in_catalog, status, owner, tags, notes, reviewed_at, "
                + ", ".join(row)
                + ") values (1, 'active', '', '[]', '', '', "
                + ", ".join(f":{k}" for k in row)
                + ")",
                row,
            )
            added.append(cid)
            continue
        if _contract_fingerprint(prev) != _contract_fingerprint(row):
            changed.append(cid)
        if _maintained(prev):
            preserved.append(cid)
        con.execute(
            "update capabilities set " + ", ".join(f"{f}=:{f}" for f in row) + ", in_catalog=1 "
            "where capability_id=:capability_id",
            row,
        )
        if not int(prev.get("in_catalog") or 0):
            restored.append(cid)
            con.execute(
                "insert into events (at, capability_id, field, old_value, new_value, actor) values (?,?,?,?,?,?)",
                (now, cid, "in_catalog", "0", "1", "import"),
            )

    for cid, prev in existing.items():
        if cid in incoming or not int(prev.get("in_catalog") or 0):
            continue
        con.execute("update capabilities set in_catalog=0, updated_at=? where capability_id=?", (now, cid))
        con.execute(
            "insert into events (at, capability_id, field, old_value, new_value, actor) values (?,?,?,?,?,?)",
            (now, cid, "in_catalog", "1", "0", "import"),
        )
        removed.append(cid)

    _import_relations(con, catalog, now)
    cur = con.execute(
        "insert into imports (imported_at, source_repo, source_commit, live_source, live_count, "
        "generated_at, caps_count, added, removed, changed, preserved, note) values (?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            now,
            str((catalog.get("source") or {}).get("repo") or ""),
            str((catalog.get("source") or {}).get("commit") or ""),
            str((catalog.get("source") or {}).get("live_source") or ""),
            int((catalog.get("source") or {}).get("live_count") or 0),
            str(catalog.get("generated_at") or ""),
            len(incoming),
            _dumps(sorted(added)),
            _dumps(sorted(removed)),
            _dumps(sorted(changed)),
            _dumps(sorted(preserved)),
            note,
        ),
    )
    con.commit()
    return {
        "import_id": cur.lastrowid,
        "imported_at": now,
        "added": sorted(added),
        "changed": sorted(changed),
        "removed": sorted(removed),
        "restored": sorted(restored),
        "preserved": sorted(preserved),
        "counts": {"capabilities": len(incoming), "preserved_annotations": len(preserved)},
    }


def _maintained(prev: dict[str, Any]) -> bool:
    """这条能力有没有被人维护过（集市字段非默认）。"""
    return bool(prev.get("status") and prev["status"] != "active") or bool(prev.get("owner")) or bool(
        prev.get("notes")
    ) or bool(_json_list(prev.get("tags")))


def _import_relations(con: sqlite3.Connection, catalog: dict[str, Any], now: str) -> None:
    """服务 / 条件声明 / 能力包 / 条件声明归属 / 线上实况（都是生成物，每次全量替换）。"""
    for table in ("services", "service_capabilities", "declared_lists", "packages", "capability_packages"):
        con.execute(f"delete from {table}")
    con.execute("delete from live")
    for svc in catalog.get("services") or []:
        sid = str(svc.get("service_id") or "").strip()
        if not sid:
            continue
        con.execute(
            "insert or replace into services (service_id, display_name, group_id, version, constant, updated_at) "
            "values (?,?,?,?,?,?)",
            (sid, svc.get("display_name") or "", svc.get("group") or "", svc.get("version") or "",
             svc.get("constant") or "", now),
        )
        for cid in svc.get("capabilities") or []:
            con.execute(
                "insert or ignore into service_capabilities (service_id, capability_id) values (?,?)", (sid, str(cid))
            )
    for cap in catalog.get("capabilities") or []:
        cid = str(cap.get("capability_id") or "").strip()
        if not cid:
            continue
        # capability 自述的归属（导出器的 declared_by）：保证「条件声明」的能力也有服务归属
        for sid in cap.get("declared_by") or []:
            con.execute("insert or ignore into services (service_id, updated_at) values (?,?)", (str(sid), now))
            con.execute(
                "insert or ignore into service_capabilities (service_id, capability_id) values (?,?)", (str(sid), cid)
            )
        for name in cap.get("declared_lists") or []:
            con.execute("insert or ignore into declared_lists (capability_id, list_name) values (?,?)", (cid, str(name)))
        for pkg in cap.get("packages") or []:
            con.execute("insert or ignore into capability_packages (capability_id, package) values (?,?)", (cid, str(pkg)))
        for prov in (cap.get("live") or {}).get("providers") or []:
            con.execute(
                "insert or replace into live (capability_id, edge_id, edge_name, assigned_edge_id, service_id, "
                "kind, role, planner_recognize, observed_at) values (?,?,?,?,?,?,?,?,?)",
                (
                    cid,
                    str(prov.get("edge_id") or ""),
                    str(prov.get("edge_name") or ""),
                    str(prov.get("assigned_edge_id") or ""),
                    str(prov.get("service_id") or ""),
                    str((cap.get("live") or {}).get("kind") or ""),
                    str((cap.get("live") or {}).get("role") or ""),
                    str((cap.get("live") or {}).get("planner_recognize") or ""),
                    now,
                ),
            )
    for pkg in catalog.get("capability_packages_meta") or []:  # 可选：导出器若给了包元数据
        con.execute(
            "insert or replace into packages (package, service_id, group_id, display_name, entry_mac, docs, "
            "config_keys, updated_at) values (?,?,?,?,?,?,?,?)",
            (
                str(pkg.get("package") or ""),
                str(pkg.get("service_id") or ""),
                str(pkg.get("group") or ""),
                str(pkg.get("display_name") or ""),
                str(pkg.get("entry_mac") or ""),
                str(pkg.get("docs") or ""),
                _dumps(pkg.get("config_keys") or []),
                now,
            ),
        )


def _row_to_cap(row: sqlite3.Row, *, live: list[dict[str, Any]] | None = None, **extra: Any) -> dict[str, Any]:
    """DB 行 → 对外 JSON（含集市字段与 reconcile）。"""
    cap = dict(row)
    for key in ("typical_triggers", "do_not_dispatch", "decomposes_to", "input_schema", "output_schema",
                "definition_sources", "tags"):
        if key in cap:
            cap[key] = _loads(cap[key], [] if key.endswith("s") and key not in ("input_schema", "output_schema") else {})
    if "tags" in cap and not isinstance(cap["tags"], list):
        cap["tags"] = []
    cap.pop("search_blob", None)
    cap["in_ads"] = bool(cap.get("in_ads"))
    cap["has_checker"] = bool(cap.get("has_checker"))
    cap["in_catalog"] = bool(cap.get("in_catalog", 1))
    live = live or []
    cap["live"] = live
    cap["in_live"] = bool(live)
    providers = [
        {"edge_id": l.get("edge_id") or "", "edge_name": l.get("edge_name") or "",
         "assigned_edge_id": l.get("assigned_edge_id") or "", "service_id": l.get("service_id") or ""}
        for l in live
    ]
    cap["providers"] = providers
    cap["reconcile"] = {
        "declared_not_live": bool(cap["in_ads"] or cap.get("declared_by") or cap.get("declared_lists")) and not cap["in_live"],
        "live_not_declared": cap["in_live"] and not cap["in_ads"],
        "not_in_catalog": not cap["in_catalog"],
    }
    cap.update(extra)
    return cap


def _live_map(con: sqlite3.Connection, ids: list[str]) -> dict[str, list[dict[str, Any]]]:
    if not ids:
        return {}
    out: dict[str, list[dict[str, Any]]] = {}
    for i in range(0, len(ids), 400):
        part = ids[i : i + 400]
        q = "select * from live where capability_id in (" + ",".join("?" * len(part)) + ")"
        for row in con.execute(q, part):
            out.setdefault(row["capability_id"], []).append(dict(row))
    return out


def list_capabilities(con: sqlite3.Connection, **f: Any) -> dict[str, Any]:
    """服务端查询：关键字 / group / kind / 设备 / 状态 / 标签 / 责任人 / 在线 / 是否在目录。"""
    where: list[str] = []
    params: list[Any] = []
    where.append("in_catalog = 1" if f.get("in_catalog") in (None, True, 1, "1") else "1=1")
    for token in str(f.get("q") or "").strip().split():
        where.append("search_blob like ?")
        params.append(f"%{token.lower()}%")
    for key, col in (("group", "group_id"), ("kind", "kind"), ("status", "status"), ("owner", "owner")):
        if f.get(key):
            where.append(f"{col} = ?")
            params.append(str(f[key]))
    if f.get("tag"):
        where.append("tags like ?")
        params.append(f'%"{f["tag"]}"%')
    if f.get("has_checker") in (True, "1", 1, "true"):
        where.append("has_checker = 1")
    if f.get("edge"):
        where.append(
            "exists (select 1 from live l where l.capability_id = capabilities.capability_id "
            "and (l.edge_name = ? or l.edge_id = ? or l.service_id = ?))"
        )
        params.extend([str(f["edge"])] * 3)
    exists_live = "exists (select 1 from live l where l.capability_id = capabilities.capability_id)"
    lf = str(f.get("live") or "")
    if lf in ("1", "true", "yes", "live"):
        where.append(exists_live)
    elif lf == "declared_not_live":
        where.append(f"in_ads = 1 and not {exists_live}")
    elif lf == "live_not_declared":
        where.append(f"in_ads = 0 and {exists_live}")

    where_sql = " and ".join(where)
    total = con.execute(f"select count(*) from capabilities where {where_sql}", params).fetchone()[0]
    order = {
        "group": "group_id, capability_id",
        "status": "status, capability_id",
        "updated": "updated_at desc, capability_id",
        "live": f"{exists_live} desc, capability_id",
    }.get(str(f.get("sort") or ""), "capability_id")
    limit = max(1, min(int(f.get("limit") or 200), 2000))
    offset = max(0, int(f.get("offset") or 0))
    rows = list(
        con.execute(
            f"select * from capabilities where {where_sql} order by {order} limit ? offset ?",
            params + [limit, offset],
        )
    )
    live = _live_map(con, [r["capability_id"] for r in rows])
    caps = [_row_to_cap(r, live=live.get(r["capability_id"], [])) for r in rows]
    return {"total": total, "count": len(caps), "offset": offset, "limit": limit, "capabilities": caps}


def _blob_extras(con: sqlite3.Connection, cid: str) -> list[str]:
    """搜索 blob 的补充文本：服务 / 条件声明 / 能力包 / 配置键 / 设备名。"""
    out: list[str] = []
    out += [r["service_id"] for r in con.execute("select service_id from service_capabilities where capability_id=?", (cid,))]
    out += [r["list_name"] for r in con.execute("select list_name from declared_lists where capability_id=?", (cid,))]
    out += [r["package"] for r in con.execute("select package from capability_packages where capability_id=?", (cid,))]
    for r in con.execute("select edge_name, edge_id, service_id from live where capability_id=?", (cid,)):
        out += [r["edge_name"] or "", r["edge_id"] or "", r["service_id"] or ""]
    return out


def get_capability(con: sqlite3.Connection, capability_id: str) -> dict[str, Any] | None:
    row = con.execute("select * from capabilities where capability_id = ?", (capability_id,)).fetchone()
    if row is None:
        return None
    cid = row["capability_id"]
    cap = _row_to_cap(row, live=_live_map(con, [cid]).get(cid, []))
    cap["declared_by"] = [r[0] for r in con.execute(
        "select service_id from service_capabilities where capability_id=?", (cid,))]
    cap["declared_lists"] = [r[0] for r in con.execute(
        "select list_name from declared_lists where capability_id=?", (cid,))]
    cap["packages"] = [r[0] for r in con.execute(
        "select package from capability_packages where capability_id=?", (cid,))]
    cap["services"] = [
        dict(r)
        for r in con.execute(
            "select s.* from services s join service_capabilities sc on sc.service_id = s.service_id "
            "where sc.capability_id = ?",
            (cid,),
        )
    ]
    cap["events"] = list_events(con, capability_id=cid, limit=50)
    return cap


def annotate(
    con: sqlite3.Connection, capability_id: str, fields: dict[str, Any], *, actor: str = "api"
) -> dict[str, Any] | None:
    """改**集市自有字段**（status/owner/tags/notes/reviewed_at）并留审计；生成物字段改不动。"""
    row = con.execute("select * from capabilities where capability_id = ?", (capability_id,)).fetchone()
    if row is None:
        return None
    now = now_iso()
    updates: dict[str, Any] = {}
    if "status" in fields:
        status = str(fields["status"] or "").strip()
        if status not in VALID_STATUS:
            raise ValueError("status 只能是 " + "/".join(VALID_STATUS))
        updates["status"] = status
    if "owner" in fields:
        updates["owner"] = str(fields["owner"] or "").strip()
    if "notes" in fields:
        updates["notes"] = str(fields["notes"] or "").strip()
    if "tags" in fields:
        tags = fields["tags"]
        if isinstance(tags, str):
            tags = tags.replace("，", ",").split(",")
        updates["tags"] = _dumps(sorted({str(t).strip() for t in (tags or []) if str(t).strip()}))
    if "reviewed_at" in fields:
        updates["reviewed_at"] = str(fields["reviewed_at"] or "")
    if not updates:
        return get_capability(con, capability_id)
    keys = set(row.keys())
    for key, value in updates.items():
        old = row[key] if key in keys else ""
        if str(old) != str(value):
            con.execute(
                "insert into events (at, capability_id, field, old_value, new_value, actor) values (?,?,?,?,?,?)",
                (now, capability_id, key, str(old), str(value), actor),
            )
    if "reviewed_at" not in updates and ("status" in updates or "notes" in updates):
        updates["reviewed_at"] = now
    updates["updated_at"] = now
    con.execute(
        "update capabilities set " + ", ".join(f"{k}=:{k}" for k in updates) + " where capability_id=:capability_id",
        {**updates, "capability_id": capability_id},
    )
    fresh = dict(con.execute("select * from capabilities where capability_id=?", (capability_id,)).fetchone())
    con.execute(
        "update capabilities set search_blob=? where capability_id=?",
        (build_search_blob(fresh, extra=_blob_extras(con, capability_id)), capability_id),
    )
    con.commit()
    return get_capability(con, capability_id)


def facets(con: sqlite3.Connection, *, in_catalog: bool = True) -> dict[str, Any]:
    """筛选项统计（UI 的 group / kind / 设备 / 状态 / 标签下拉）。"""
    cond = "in_catalog = 1" if in_catalog else "1=1"
    def counts(sql: str, params: tuple = ()) -> list[dict[str, Any]]:
        return [{"name": r[0], "count": r[1]} for r in con.execute(sql, params) if r[0]]

    groups = counts(f"select group_id, count(*) c from capabilities where {cond} group by group_id order by c desc, group_id")
    kinds = counts(f"select kind, count(*) c from capabilities where {cond} group by kind order by c desc, kind")
    statuses = counts(f"select status, count(*) c from capabilities where {cond} group by status order by status")
    edges = counts("select edge_name, count(distinct capability_id) c from live group by edge_name order by c desc")
    services = counts(
        "select s.service_id, count(distinct sc.capability_id) c from services s "
        "join service_capabilities sc on sc.service_id = s.service_id group by s.service_id order by c desc, s.service_id"
    )
    tags: dict[str, int] = {}
    for r in con.execute(f"select tags from capabilities where {cond}"):
        for t in _json_list(r[0]):
            tags[t] = tags.get(t, 0) + 1
    return {
        "groups": groups,
        "kinds": kinds,
        "statuses": statuses,
        "edges": edges,
        "services": services,
        "tags": [{"name": k, "count": v} for k, v in sorted(tags.items(), key=lambda kv: (-kv[1], kv[0]))],
    }


def stats(con: sqlite3.Connection) -> dict[str, Any]:
    one = lambda sql, p=(): con.execute(sql, p).fetchone()[0]  # noqa: E731
    last = con.execute("select * from imports order by import_id desc limit 1").fetchone()
    return {
        "capabilities": one("select count(*) from capabilities where in_catalog = 1"),
        "not_in_catalog": one("select count(*) from capabilities where in_catalog = 0"),
        "live": one("select count(distinct capability_id) from live"),
        "services": one("select count(*) from services"),
        "packages": one("select count(*) from packages"),
        "declared_lists": one("select count(distinct capability_id) from declared_lists"),
        "with_checker": one("select count(*) from capabilities where has_checker = 1 and in_catalog = 1"),
        "annotated": one(
            "select count(*) from capabilities where in_catalog = 1 and "
            "(status != 'active' or owner != '' or notes != '' or tags != '[]')"
        ),
        "statuses": {
            r[0]: r[1] for r in con.execute("select status, count(*) from capabilities where in_catalog=1 group by status")
        },
        "schema_version": one("select value from meta where key='schema_version'"),
        "imports": one("select count(*) from imports"),
        "last_import": dict(last) if last is not None else None,
    }


def list_imports(con: sqlite3.Connection, *, limit: int = 20) -> list[dict[str, Any]]:
    rows = con.execute("select * from imports order by import_id desc limit ?", (max(1, int(limit)),))
    out = []
    for row in rows:
        item = dict(row)
        for key in ("added", "removed", "changed", "preserved"):
            item[key] = _loads(item[key], [])
        out.append(item)
    return out


def list_events(
    con: sqlite3.Connection, *, capability_id: str = "", limit: int = 50
) -> list[dict[str, Any]]:
    if capability_id:
        rows = con.execute(
            "select * from events where capability_id = ? order by event_id desc limit ?",
            (capability_id, max(1, int(limit))),
        )
    else:
        rows = con.execute("select * from events order by event_id desc limit ?", (max(1, int(limit)),))
    return [dict(r) for r in rows]


def export_catalog(con: sqlite3.Connection) -> dict[str, Any]:
    """DB → catalog JSON（**集市导出**：含集市字段注解），供静态 UI/Pages、diff 与外部消费。

    与导出器的 catalog 同 schema，但多三样：每条能力的 `status/owner/tags/notes`（集市自有字段）、
    `reconcile.not_in_catalog`（代码里已没了）、以及 summary 里的注解统计。
    """
    rows = list(con.execute("select * from capabilities order by capability_id"))
    live = _live_map(con, [r["capability_id"] for r in rows])
    last = con.execute("select * from imports order by import_id desc limit 1").fetchone()
    caps: list[dict[str, Any]] = []
    for row in rows:
        cid = row["capability_id"]
        item = _row_to_cap(row, live=live.get(cid, []))
        item["definition"] = {
            "kind": item["kind"],
            "composition": item["composition"],
            "group": item["group_id"],
            "display_name": item["display_name"],
            "role": item["role"],
            "planner_recognize": item["planner_recognize"],
            "prefer_when": item["prefer_when"],
            "typical_triggers": item["typical_triggers"],
            "do_not_dispatch": item["do_not_dispatch"],
            "decomposes_to": item["decomposes_to"],
            "input_schema": item["input_schema"],
            "output_schema": item["output_schema"],
            "sources": item["definition_sources"],
        }
        item["group"] = item.pop("group_id")
        # live 形状与导出器一致（对象 + providers），让两种 catalog **可互换导入**
        providers = item.get("providers") or []
        live_rows = item.get("live") or []
        first = live_rows[0] if live_rows else {}
        item["live"] = {
            "kind": first.get("kind") or item["kind"],
            "role": first.get("role") or item["role"],
            "planner_recognize": first.get("planner_recognize") or item["planner_recognize"],
            "typical_triggers": item.get("typical_triggers") or [],
            "do_not_dispatch": item.get("do_not_dispatch") or [],
            "input_schema": item.get("input_schema") or {},
            "output_schema": item.get("output_schema") or {},
            "providers": providers,
        } if live_rows else {}
        item["declared_by"] = [r[0] for r in con.execute(
            "select service_id from service_capabilities where capability_id=?", (cid,))]
        item["declared_lists"] = [r[0] for r in con.execute(
            "select list_name from declared_lists where capability_id=?", (cid,))]
        item["packages"] = [r[0] for r in con.execute(
            "select package from capability_packages where capability_id=?", (cid,))]
        caps.append(item)

    current = [c for c in caps if c["in_catalog"]]
    groups: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for cap in current:
        groups[cap["group"] or "(未分类)"] = groups.get(cap["group"] or "(未分类)", 0) + 1
        kinds[cap["kind"] or "(未标注)"] = kinds.get(cap["kind"] or "(未标注)", 0) + 1
    gen_at = now_iso()
    return {
        "schema": "home-agent.capability-catalog/v1",
        "generated_by": "marketplace-db (server/catalog_cli.py export)",
        "generated_at": gen_at,
        "source": {
            "repo": (last["source_repo"] if last is not None else "") or "",
            "commit": (last["source_commit"] if last is not None else "") or "",
            "edge": "mac_edge",
            "live_source": (last["live_source"] if last is not None else "") or "",
            "live_count": int((last["live_count"] if last is not None else 0) or 0),
            "imported_at": (last["imported_at"] if last is not None else "") or "",
        },
        "summary": {
            "capabilities": len(current),
            "not_in_catalog": len(caps) - len(current),
            "live": sum(1 for c in current if c["in_live"]),
            "declared_not_live": sum(1 for c in current if c["reconcile"]["declared_not_live"]),
            "live_not_declared": sum(1 for c in current if c["reconcile"]["live_not_declared"]),
            "with_checker": sum(1 for c in current if c["has_checker"]),
            "annotated": sum(1 for c in current if _maintained(c)),
            "updated": sum(1 for c in current if c.get("reviewed_at")),
            "groups": dict(sorted(groups.items())),
            "kinds": dict(sorted(kinds.items())),
        },
        "services": [dict(r) for r in con.execute("select * from services order by service_id")],
        "capabilities": caps,
    }








