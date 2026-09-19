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

SCHEMA_VERSION = 4
# 集市自有字段（导入永不覆盖）：人在这里写「描述」「关键字」「适用宿主」，补代码生成物说不清的语义
MARKETPLACE_FIELDS = ("status", "owner", "tags", "notes", "description", "keywords", "hosts", "reviewed_at")
# 宿主（capability 的适用宿主）默认元数据：代码里只给一个 id（mac/brain/…），这里给可读名字
# 说明：id 来自 manifest 的 platforms / entry 键；人工可以在集市里改名、写备注、标状态
HOST_DEFAULTS: dict[str, dict[str, str]] = {
    "mac": {"display_name": "Mac Edge（本机 macOS）", "kind": "edge"},
    "brain": {"display_name": "Brain（服务端）", "kind": "server"},
    "ios": {"display_name": "iOS App", "kind": "mobile"},
    "android": {"display_name": "Android App", "kind": "mobile"},
    "python": {"display_name": "Python 运行时（随宿主进程）", "kind": "runtime"},
    "cloud": {"display_name": "云端", "kind": "cloud"},
}
VALID_HOST_STATUS = ("active", "planned", "deprecated", "blocked")
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
  -- 人工维护：描述（展示用）、关键字（搜索/归类用）、适用宿主（人工可改）
  description text not null default '', keywords text not null default '[]',
  hosts text not null default '[]',
  -- 代码事实：manifest 的 platforms/entry 键（导入即覆盖）
  runs_on text not null default '[]',
  reviewed_at text not null default '', updated_at text not null default '',
  in_catalog integer not null default 1,
  search_blob text not null default ''
);

create table if not exists hosts (
  host_id text primary key, display_name text not null default '',
  kind text not null default 'platform', notes text not null default '',
  status text not null default 'active', curated integer not null default 0,
  updated_at text not null default ''
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
create index if not exists idx_pkg_cap on capability_packages(capability_id);
"""


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _migrate(con: sqlite3.Connection) -> None:
    """老库补列：`create table if not exists` 不会给已存在的表加列。

    历史：v2 弃用 `live` 表（集市不再存实时状态）；v3 增加人工维护的 `description` / `keywords`。
    """
    have = {str(r[1]) for r in con.execute("pragma table_info(capabilities)")}
    for column, ddl in (
        ("description", "text not null default ''"),
        ("keywords", "text not null default '[]'"),
        ("hosts", "text not null default '[]'"),
        ("runs_on", "text not null default '[]'"),
    ):
        if column not in have:
            con.execute(f"alter table capabilities add column {column} {ddl}")


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
    _migrate(con)
    # v2：集市只登记「声明」，不再保存实时状态 —— 老库里的 live 表清掉
    con.execute("drop table if exists live")
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


def _clean_text(value: Any, limit: int, label: str) -> str:
    """人工写的文本：去首尾空白 + 限长（超长直接报错，别静默截断）。"""
    text = str(value if value is not None else "").strip()
    if len(text) > limit:
        raise ValueError(f"{label}最长 {limit} 字（当前 {len(text)}）")
    return text


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
        str(row.get("description") or ""),
    ]
    for key in ("typical_triggers", "do_not_dispatch", "decomposes_to", "definition_sources", "tags", "keywords"):
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
    "input_schema", "output_schema", "definition_sources", "has_checker", "in_ads", "runs_on",
)


def _contract_fingerprint(row: dict[str, Any]) -> str:
    """生成物字段的指纹：用来判断「代码里的契约变了」。"""
    return json.dumps({k: row.get(k) for k in GENERATOR_FIELDS}, ensure_ascii=False, sort_keys=True)


def _declared_by(cap: dict[str, Any]) -> list[str]:
    """归属服务：导出器版在顶层 declared_by；集市导出在 declaration.declared_by。"""
    raw = cap.get("declared_by") or (cap.get("declaration") or {}).get("declared_by") or []
    return [str(x) for x in raw]


def _declared_lists(cap: dict[str, Any]) -> list[str]:
    """条件声明常量名（两种形状都认）。"""
    raw = (
        cap.get("conditional_lists")
        or cap.get("declared_lists")
        or (cap.get("declaration") or {}).get("conditional_lists")
        or []
    )
    return [str(x) for x in raw]


def _package_names(cap: dict[str, Any]) -> list[str]:
    raw = cap.get("packages") or (cap.get("declaration") or {}).get("packages") or []
    return [str(x) for x in raw]


def _has_preflight(cap: dict[str, Any]) -> bool:
    """有没有「执行前自检」（静态声明；集市不做任何探测）。"""
    return bool(
        (cap.get("availability") or {}).get("has_checker")
        or cap.get("has_preflight")
        or (cap.get("declaration") or {}).get("has_preflight")
    )


def _pkg_hints(cap: dict[str, Any]) -> list[str]:
    """额外参与搜索的文本：服务/包/配置键/声明列表/设备名。"""
    out: list[str] = []
    out.extend(_declared_by(cap))
    out.extend(_declared_lists(cap))
    out.extend(_package_names(cap))
    for key in ("docs", "config_keys"):
        out.extend(str(x) for x in (cap.get(key) or []))
    return out


def _cap_row(cap: dict[str, Any], *, now: str, extra: Iterable[str] = ()) -> dict[str, Any]:
    """把 catalog 里的一条能力摊平成 DB 行（生成物字段）。"""
    definition = cap.get("definition") or {}
    row: dict[str, Any] = {
        "capability_id": str(cap.get("capability_id") or "").strip(),
        "kind": str(cap.get("kind") or definition.get("kind") or ""),
        "composition": str(cap.get("composition") or definition.get("composition") or "atomic"),
        "group_id": str(cap.get("group") or definition.get("group") or ""),
        "display_name": str(cap.get("display_name") or definition.get("display_name") or ""),
        "role": str(cap.get("role") or definition.get("role") or ""),
        "planner_recognize": str(definition.get("planner_recognize") or cap.get("planner_recognize") or ""),
        "prefer_when": str(definition.get("prefer_when") or ""),
        "typical_triggers": _dumps(definition.get("typical_triggers") or cap.get("typical_triggers") or []),
        "do_not_dispatch": _dumps(definition.get("do_not_dispatch") or cap.get("do_not_dispatch") or []),
        "decomposes_to": _dumps(definition.get("decomposes_to") or []),
        "input_schema": _dumps(definition.get("input_schema") or cap.get("input_schema") or {}),
        "output_schema": _dumps(definition.get("output_schema") or cap.get("output_schema") or {}),
        "definition_sources": _dumps(definition.get("sources") or []),
        "has_checker": int(_has_preflight(cap)),
        "in_ads": int(bool(cap.get("in_ads"))),
        "runs_on": _dumps([str(h) for h in sorted(dict.fromkeys(cap.get("runs_on") or [])) if str(h).strip()]),
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

    cols = (
        "select capability_id, in_catalog, status, owner, tags, notes, description, keywords, hosts, "
        + ", ".join(GENERATOR_FIELDS)
        + " from capabilities"
    )
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
    _sync_hosts(con, now)
    # search_blob 是「生成物 + 人工字段 + 关系」的并集：关系刚更新完，这里统一重建一遍，
    # 否则导入会用「只含生成物」的 blob 覆盖掉人工写的描述/关键字/owner/notes（搜不到）。
    for (cid,) in list(con.execute("select capability_id from capabilities")):
        row = dict(con.execute("select * from capabilities where capability_id=?", (cid,)).fetchone())
        con.execute(
            "update capabilities set search_blob=? where capability_id=?",
            (build_search_blob(row, extra=_blob_extras(con, cid)), cid),
        )
    cur = con.execute(
        "insert into imports (imported_at, source_repo, source_commit, "
        "generated_at, caps_count, added, removed, changed, preserved, note) values (?,?,?,?,?,?,?,?,?,?)",
        (
            now,
            str((catalog.get("source") or {}).get("repo") or ""),
            str((catalog.get("source") or {}).get("commit") or ""),
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
    return (
        bool(prev.get("status") and prev["status"] != "active")
        or bool(prev.get("owner"))
        or bool(prev.get("notes"))
        or bool(prev.get("description"))
        or bool(_json_list(prev.get("hosts")))
        or bool(_json_list(prev.get("tags")))
        or bool(_json_list(prev.get("keywords")))
    )


def _sync_hosts(con: sqlite3.Connection, now: str) -> None:
    """宿主注册表：把「代码声明的 + 人工设置的」宿主都登记进来（人工改过的元数据不动）。

    宿主 id 只从事实出发（manifest 的 platforms/entry 键，或人工设置里写的新 id）；
    显示名/分类取 HOST_DEFAULTS，人工可以在集市里改名、写备注、标状态（curated=1）。
    """
    seen: set[str] = set()
    for row in con.execute("select runs_on, hosts from capabilities"):
        seen.update(_json_list(row[0]))
        seen.update(_json_list(row[1]))
    for host_id in sorted(seen):
        if con.execute("select 1 from hosts where host_id=?", (host_id,)).fetchone() is None:
            meta = HOST_DEFAULTS.get(host_id, {})
            con.execute(
                "insert into hosts (host_id, display_name, kind, notes, status, curated, updated_at) "
                "values (?,?,?,?,'active',0,?)",
                (host_id, meta.get("display_name") or host_id, meta.get("kind") or "platform",
                 meta.get("notes") or "", now),
            )


def _import_relations(con: sqlite3.Connection, catalog: dict[str, Any], now: str) -> None:
    """服务 / 条件声明 / 能力包 / 条件声明归属 / 线上实况（都是生成物，每次全量替换）。"""
    for table in ("services", "service_capabilities", "declared_lists", "packages", "capability_packages"):
        con.execute(f"delete from {table}")
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
        for sid in _declared_by(cap):
            con.execute("insert or ignore into services (service_id, updated_at) values (?,?)", (str(sid), now))
            con.execute(
                "insert or ignore into service_capabilities (service_id, capability_id) values (?,?)", (str(sid), cid)
            )
        for name in _declared_lists(cap):
            con.execute("insert or ignore into declared_lists (capability_id, list_name) values (?,?)", (cid, str(name)))
        for pkg in _package_names(cap):
            con.execute("insert or ignore into capability_packages (capability_id, package) values (?,?)", (cid, str(pkg)))
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


def _row_to_cap(row: sqlite3.Row, **extra: Any) -> dict[str, Any]:
    """DB 行 → 对外 JSON（**声明视图**：归属/条件声明/能力包 + 集市字段）。

    刻意不含任何实时状态（在线/设备/探测结果）—— 集市是「能力展示与技能介绍」，
    实时状态以 Brain 的在线注册表为准，不在这里重复。
    """
    cap = dict(row)
    for key in ("input_schema", "output_schema"):
        if key in cap:
            cap[key] = _loads(cap[key], {})
    for key in ("typical_triggers", "do_not_dispatch", "decomposes_to", "definition_sources", "tags",
                "keywords", "runs_on", "hosts"):
        if key in cap:
            value = _loads(cap[key], [])
            cap[key] = value if isinstance(value, list) else []
    cap.pop("search_blob", None)
    # list 查询用 GROUP_CONCAT 带出来的归属/包/条件声明（列表页也要显示「谁提供」）
    cap["declared_by"] = sorted(x for x in str(cap.pop("declared_by_csv", "") or "").split(",") if x)
    cap["packages"] = sorted(x for x in str(cap.pop("packages_csv", "") or "").split(",") if x)
    cap["conditional_lists"] = sorted(x for x in str(cap.pop("lists_csv", "") or "").split(",") if x)
    cap["in_ads"] = bool(cap.get("in_ads"))
    cap["declared"] = bool(cap["in_ads"] or cap["declared_by"] or cap["conditional_lists"])
    cap["has_preflight"] = bool(cap.get("has_checker"))
    cap["in_catalog"] = bool(cap.get("in_catalog", 1))
    # 适用宿主：人工设置的优先，否则用代码事实（manifest 的 platforms/entry）
    cap["hosts_effective"] = list(cap["hosts"]) or list(cap["runs_on"])
    cap["hosts_source"] = "curated" if cap["hosts"] else ("code" if cap["runs_on"] else "none")
    cap.update(extra)
    return cap


def list_capabilities(con: sqlite3.Connection, **f: Any) -> dict[str, Any]:
    """服务端查询（**声明维度**）：关键字 / group / kind / 服务 / 集市状态 / 标签 / 责任人 /
    条件声明 / 有执行前自检 / 有无文档。

    没有任何实时状态参数（在线、设备）—— 集市只登记声明。
    """
    joins = [
        "(select group_concat(sc.service_id) from service_capabilities sc where sc.capability_id = c.capability_id) as declared_by_csv",
        "(select group_concat(cp.package) from capability_packages cp where cp.capability_id = c.capability_id) as packages_csv",
        "(select group_concat(dl.list_name) from declared_lists dl where dl.capability_id = c.capability_id) as lists_csv",
    ]
    select = "select c.*, " + ", ".join(joins) + " from capabilities c"
    where: list[str] = []
    params: list[Any] = []
    where.append("c.in_catalog = 1" if f.get("in_catalog") in (None, True, 1, "1") else "1=1")
    for token in str(f.get("q") or "").strip().split():
        where.append("c.search_blob like ?")
        params.append(f"%{token.lower()}%")
    for key, col in (("group", "c.group_id"), ("kind", "c.kind"), ("status", "c.status"), ("owner", "c.owner")):
        if f.get(key):
            where.append(f"{col} = ?")
            params.append(str(f[key]))
    if f.get("tag"):
        where.append("c.tags like ?")
        params.append(f'%"{f["tag"]}"%')
    if f.get("host"):
        # 有效宿主：人工设置优先，否则代码事实
        where.append("(case when c.hosts != '[]' then c.hosts else c.runs_on end) like ?")
        params.append(f'%"{f["host"]}"%')
    if f.get("keyword"):
        where.append("c.keywords like ?")
        params.append(f'%"{f["keyword"]}"%')
    if f.get("described") in (True, "1", 1, "true"):
        where.append("c.description != ''")
    if f.get("service"):
        where.append("exists (select 1 from service_capabilities sc where sc.capability_id = c.capability_id and sc.service_id = ?)")
        params.append(str(f["service"]))
    if f.get("preflight") in (True, "1", 1, "true"):
        where.append("c.has_checker = 1")
    if f.get("conditional") in (True, "1", 1, "true"):
        where.append("exists (select 1 from declared_lists dl where dl.capability_id = c.capability_id)")
    if f.get("documented") in (True, "1", 1, "true"):
        where.append("exists (select 1 from capability_packages cp where cp.capability_id = c.capability_id)")

    where_sql = " and ".join(where)
    total = con.execute(f"select count(*) from capabilities c where {where_sql}", params).fetchone()[0]
    order = {
        "group": "c.group_id, c.capability_id",
        "status": "c.status, c.capability_id",
        "updated": "c.updated_at desc, c.capability_id",
    }.get(str(f.get("sort") or ""), "c.capability_id")
    limit = max(1, min(int(f.get("limit") or 200), 2000))
    offset = max(0, int(f.get("offset") or 0))
    rows = list(con.execute(f"{select} where {where_sql} order by {order} limit ? offset ?", params + [limit, offset]))
    caps = [_row_to_cap(r) for r in rows]
    return {"total": total, "count": len(caps), "offset": offset, "limit": limit, "capabilities": caps}


def _blob_extras(con: sqlite3.Connection, cid: str) -> list[str]:
    """搜索 blob 的补充文本：服务 / 条件声明 / 能力包 / 适用宿主（都是声明，不含实时信息）。"""
    out: list[str] = []
    row = con.execute("select hosts, runs_on from capabilities where capability_id=?", (cid,)).fetchone()
    if row is not None:
        for host in (_json_list(row[0]) or _json_list(row[1])):
            out.append(host)
            meta = con.execute("select display_name, notes from hosts where host_id=?", (host,)).fetchone()
            if meta is not None:
                out += [meta[0] or "", meta[1] or ""]
    out += [r["service_id"] for r in con.execute("select service_id from service_capabilities where capability_id=?", (cid,))]
    out += [r["list_name"] for r in con.execute("select list_name from declared_lists where capability_id=?", (cid,))]
    out += [r["package"] for r in con.execute("select package from capability_packages where capability_id=?", (cid,))]
    return out


def get_capability(con: sqlite3.Connection, capability_id: str) -> dict[str, Any] | None:
    row = con.execute("select * from capabilities where capability_id = ?", (capability_id,)).fetchone()
    if row is None:
        return None
    cid = row["capability_id"]
    cap = _row_to_cap(row)
    cap["declared_by"] = [r[0] for r in con.execute(
        "select service_id from service_capabilities where capability_id=?", (cid,))]
    cap["conditional_lists"] = [r[0] for r in con.execute(
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
    cap["hosts_all"] = list_hosts(con)
    return cap


def list_hosts(con: sqlite3.Connection) -> list[dict[str, Any]]:
    """宿主注册表 + 用量（口径 = 有效宿主：人工设置优先，否则代码事实）。"""
    usage: dict[str, int] = {}
    for row in con.execute("select hosts, runs_on, in_catalog from capabilities"):
        if not int(row[2]):
            continue
        for host in (_json_list(row[0]) or _json_list(row[1])):
            usage[host] = usage.get(host, 0) + 1
    out: list[dict[str, Any]] = []
    for row in con.execute("select * from hosts order by host_id"):
        item = dict(row)
        item["curated"] = bool(item.get("curated"))
        item["capabilities"] = usage.get(item["host_id"], 0)
        out.append(item)
    return out


def annotate_host(
    con: sqlite3.Connection, host_id: str, fields: dict[str, Any], *, actor: str = "api"
) -> dict[str, Any] | None:
    """改宿主的展示元数据（display_name / kind / notes / status）；curated=1 后导入不再动它。"""
    row = con.execute("select * from hosts where host_id=?", (host_id,)).fetchone()
    if row is None:
        return None
    now = now_iso()
    updates: dict[str, Any] = {"curated": 1}
    if "display_name" in fields:
        updates["display_name"] = _clean_text(fields["display_name"], 120, "宿主显示名")
    if "kind" in fields:
        updates["kind"] = _clean_text(fields["kind"], 40, "宿主分类") or "platform"
    if "notes" in fields:
        updates["notes"] = _clean_text(fields["notes"], 1000, "宿主备注")
    if "status" in fields:
        status = str(fields["status"] or "").strip()
        if status not in VALID_HOST_STATUS:
            raise ValueError("宿主状态只能是 " + "/".join(VALID_HOST_STATUS))
        updates["status"] = status
    keys = set(row.keys())
    for key, value in updates.items():
        old = row[key] if key in keys else ""
        if str(old) != str(value):
            con.execute(
                "insert into events (at, capability_id, field, old_value, new_value, actor) values (?,?,?,?,?,?)",
                (now, "host:" + host_id, key, str(old), str(value), actor),
            )
    updates["updated_at"] = now
    con.execute(
        "update hosts set " + ", ".join(f"{k}=:{k}" for k in updates) + " where host_id=:host_id",
        {**updates, "host_id": host_id},
    )
    con.commit()
    for item in list_hosts(con):
        if item["host_id"] == host_id:
            return item
    return None


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
    if "description" in fields:
        updates["description"] = _clean_text(fields["description"], 2000, "描述")
    if "keywords" in fields:
        raw = fields["keywords"]
        if isinstance(raw, str):
            raw = raw.replace("，", ",").replace("、", ",").replace(" ", ",").split(",")
        keywords = sorted({str(k).strip() for k in (raw or []) if str(k).strip()})
        if len(keywords) > 20:
            raise ValueError("关键字最多 20 个")
        for kw in keywords:
            if len(kw) > 40:
                raise ValueError("单个关键字最长 40 字")
        updates["keywords"] = _dumps(keywords)
    if "hosts" in fields:
        raw = fields["hosts"]
        if isinstance(raw, str):
            raw = raw.replace("，", ",").replace("、", ",").replace(" ", ",").split(",")
        hosts = sorted({str(h).strip() for h in (raw or []) if str(h).strip()})
        if len(hosts) > 20:
            raise ValueError("适用宿主最多 20 个")
        for host in hosts:
            if len(host) > 40:
                raise ValueError("单个宿主 id 最长 40 字")
            if con.execute("select 1 from hosts where host_id=?", (host,)).fetchone() is None:
                meta = HOST_DEFAULTS.get(host, {})
                con.execute(
                    "insert into hosts (host_id, display_name, kind, notes, status, curated, updated_at) "
                    "values (?,?,?,?,'active',0,?)",
                    (host, meta.get("display_name") or host, meta.get("kind") or "platform",
                     meta.get("notes") or "", now),
                )
        updates["hosts"] = _dumps(hosts)
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
    services = counts(
        "select s.service_id, count(distinct sc.capability_id) c from services s "
        "join service_capabilities sc on sc.service_id = s.service_id group by s.service_id order by c desc, s.service_id"
    )
    tags: dict[str, int] = {}
    keywords: dict[str, int] = {}
    host_counts: dict[str, int] = {}
    for r in con.execute(f"select tags, keywords, hosts, runs_on from capabilities where {cond}"):
        for t in _json_list(r[0]):
            tags[t] = tags.get(t, 0) + 1
        for k in _json_list(r[1]):
            keywords[k] = keywords.get(k, 0) + 1
        for h in (_json_list(r[2]) or _json_list(r[3])):
            host_counts[h] = host_counts.get(h, 0) + 1
    host_meta = {r[0]: (r[1], r[2]) for r in con.execute("select host_id, display_name, kind from hosts")}
    ordered = lambda d: [{"name": k, "count": v} for k, v in sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))]  # noqa: E731
    return {
        "groups": groups,
        "kinds": kinds,
        "statuses": statuses,
        "services": services,
        "tags": ordered(tags),
        "keywords": ordered(keywords),
        "hosts": [
            {
                "name": h,
                "count": c,
                "display_name": (host_meta.get(h) or (h, "platform"))[0] or h,
                "kind": (host_meta.get(h) or (h, "platform"))[1],
            }
            for h, c in sorted(host_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
    }


def stats(con: sqlite3.Connection) -> dict[str, Any]:
    """库概览（**声明维度**）：能力数、服务/能力包、条件声明、执行前自检、策展过的条目、导入次数。"""
    one = lambda sql, p=(): con.execute(sql, p).fetchone()[0]  # noqa: E731
    last = con.execute("select * from imports order by import_id desc limit 1").fetchone()
    return {
        "capabilities": one("select count(*) from capabilities where in_catalog = 1"),
        "not_in_catalog": one("select count(*) from capabilities where in_catalog = 0"),
        "ads_declared": one("select count(*) from capabilities where in_catalog = 1 and in_ads = 1"),
        "with_service": one(
            "select count(*) from capabilities c where c.in_catalog = 1 "
            "and exists (select 1 from service_capabilities sc where sc.capability_id = c.capability_id)"
        ),
        "conditional": one(
            "select count(*) from capabilities c where c.in_catalog = 1 "
            "and exists (select 1 from declared_lists dl where dl.capability_id = c.capability_id)"
        ),
        "with_preflight": one("select count(*) from capabilities where in_catalog = 1 and has_checker = 1"),
        "with_package": one(
            "select count(*) from capabilities c where c.in_catalog = 1 "
            "and exists (select 1 from capability_packages cp where cp.capability_id = c.capability_id)"
        ),
        "services": one("select count(*) from services"),
        "packages": one("select count(*) from packages"),
        "annotated": one(
            "select count(*) from capabilities where in_catalog = 1 and "
            "(status != 'active' or owner != '' or notes != '' or description != '' or tags != '[]' "
            "or keywords != '[]' or hosts != '[]')"
        ),
        "described": one("select count(*) from capabilities where in_catalog = 1 and description != ''"),
        "with_hosts": one(
            "select count(*) from capabilities where in_catalog = 1 and (hosts != '[]' or runs_on != '[]')"
        ),
        "hosts_curated": one("select count(*) from capabilities where in_catalog = 1 and hosts != '[]'"),
        "hosts": one("select count(*) from hosts"),
        "with_keywords": one("select count(*) from capabilities where in_catalog = 1 and keywords != '[]'"),
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
    """DB → catalog JSON（**声明导出**）：能力声明 + 归属/条件声明/能力包 + 集市策展字段。

    不含实时状态（在线/设备/探测结果）—— 集市定位是「能力展示与技能介绍」。
    实时状态看 Brain `GET /api/v1/capabilities`。
    """
    rows = list(con.execute("select * from capabilities order by capability_id"))
    last = con.execute("select * from imports order by import_id desc limit 1").fetchone()
    caps: list[dict[str, Any]] = []
    for row in rows:
        cid = row["capability_id"]
        item = _row_to_cap(row)
        item["declared_by"] = [r[0] for r in con.execute(
            "select service_id from service_capabilities where capability_id=? order by service_id", (cid,))]
        item["conditional_lists"] = [r[0] for r in con.execute(
            "select list_name from declared_lists where capability_id=? order by list_name", (cid,))]
        item["packages"] = [r[0] for r in con.execute(
            "select package from capability_packages where capability_id=? order by package", (cid,))]
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
        item["declaration"] = {
            "in_ads": item["in_ads"],
            "declared_by": item["declared_by"],
            "conditional_lists": item["conditional_lists"],
            "packages": item["packages"],
            "has_preflight": item["has_preflight"],
            "docs": [f"plugins/{pkg}/capability.md" for pkg in item["packages"]],
        }
        # 适用宿主：runs_on = 代码事实（manifest platforms/entry）；hosts = 人工设置（优先）
        item["hosts_effective"] = list(item["hosts"]) or list(item["runs_on"])
        item["hosts_source"] = "curated" if item["hosts"] else ("code" if item["runs_on"] else "none")
        item["group"] = item.pop("group_id")
        caps.append(item)

    current = [c for c in caps if c["in_catalog"]]
    groups: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for cap in current:
        groups[cap["group"] or "(未分类)"] = groups.get(cap["group"] or "(未分类)", 0) + 1
        kinds[cap["kind"] or "(未标注)"] = kinds.get(cap["kind"] or "(未标注)", 0) + 1
    return {
        "schema": "home-agent.capability-catalog/v1",
        "kind": "declaration",
        "generated_by": "marketplace-db (server/catalog_cli.py export)",
        "generated_at": now_iso(),
        "source": {
            "repo": (last["source_repo"] if last is not None else "") or "",
            "commit": (last["source_commit"] if last is not None else "") or "",
            "edge": "mac_edge",
            "imported_at": (last["imported_at"] if last is not None else "") or "",
        },
        "summary": {
            "capabilities": len(current),
            "not_in_catalog": len(caps) - len(current),
            "with_service": sum(1 for c in current if c["declared_by"]),
            "conditional": sum(1 for c in current if c["conditional_lists"]),
            "with_preflight": sum(1 for c in current if c["has_preflight"]),
            "with_package": sum(1 for c in current if c["packages"]),
            "with_hosts": sum(1 for c in current if c["hosts_effective"]),
            "hosts_curated": sum(1 for c in current if c["hosts"]),
            "annotated": sum(1 for c in current if _maintained(c)),
            "groups": dict(sorted(groups.items())),
            "kinds": dict(sorted(kinds.items())),
        },
        "services": [dict(r) for r in con.execute("select * from services order by service_id")],
        "hosts": list_hosts(con),
        "capabilities": caps,
    }
