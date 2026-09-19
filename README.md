# home-agent 能力集市（capability marketplace）

家里**所有能力的唯一登记处**：谁声明、怎么触发、参数是什么、**跑在哪些宿主上（Mac Edge / Brain / iOS…）**、
被谁认领、评审到哪一步。

定位是**能力展示与技能介绍**：只登记**静态声明**，不保存实时状态、不做设备探测。
「此刻谁在线」请查 Brain `GET /api/v1/capabilities`（在线注册表），集市不重复它。

- **有独立数据库**（SQLite）：目录 / 注解 / 导入历史都在库里，服务端可查、可改；
- **有可查 UI**：关键字、group、kind、服务归属、声明特征、集市状态多维筛选 + 详情 + 注解编辑；
- **内容自动生成**：能力定义来自 `home-agent-os` 的代码（导出器），导入库里，人只维护「集市字段」。

## 一、跑起来

```bash
# 1) 起服务（默认 :4250；库默认 ~/database/home-agent-capability-marketplace/marketplace.sqlite3）
python3 server/catalog_cli.py serve          # 或 bash scripts/start.sh（平台用的同一套）

# 2) 导入能力目录（从 home-agent-os 导出 → 入库 → 回写仓库）
scripts/sync.sh /path/to/home-agent-os

# 3) 打开 UI
open http://127.0.0.1:4250/                   # 服务版（可注解）；web/index.html 也支持静态托管
```

## 二、数据库（独立管理）

```
~/database/home-agent-capability-marketplace/marketplace.sqlite3     ← 生产库（代码与 runtime 之外）
```

**为什么要有库**（而不是只留一份 JSON）：

1. **集市自有字段**要能自己管，而且**重导入不许覆盖**：`status`(active/planned/deprecated/blocked)、
   `owner`、`tags`、`notes`、`reviewed_at`；
2. **服务端查询**：关键字（含参数说明/触发语/服务/包/配置键/owner/notes）、group、kind、服务、声明特征、标签；
3. **导入留痕**：每次导入记 `source_commit` 与增/删/改/恢复/保留注解的数量 —— 目录变化可追溯；
4. **软删**：代码里删掉的能力置 `in_catalog=0`（注解与历史都留着，代码里回来即恢复）。

| 表 | 作用 |
|---|---|
| `capabilities` | 一条能力一行：生成物字段（kind/role/触发语/schema/sources/in_ads/**runs_on**）+ **集市字段**（status/owner/tags/notes/description/keywords/**hosts**）+ `search_blob`；`in_catalog=0` = 代码里已下线（软删） |
| `hosts` | **宿主注册表**：适用宿主的 id / 可读名 / 分类 / 备注 / 状态；`curated=1` 表示人改过（导入不再动） |
| `services` / `service_capabilities` | 服务声明与归属（含「条件声明」的能力） |
| `declared_lists` | 条件声明常量（如 `AUDIO_DISPLAY_CAPABILITIES`）→ 这是「按依赖决定是否挂上」的能力 |
| `packages` / `capability_packages` | 能力包（`plugins/*/manifest.yaml` 落库） |
| `imports` | 导入历史（added / removed / changed / preserved） |
| `events` | 集市字段的审计流水（谁、何时、把哪个字段从什么改成什么） |

核心分层：**生成物字段随代码走（导入即覆盖），集市字段随人走（导入永不覆盖）**。

**适用宿主**同样是两层：`runs_on` 是**代码事实**（`plugins/*/manifest.yaml` 的 `platforms:` 与 `entry:` 键，
如 `mac` / `brain` / `ios` / `android`），导入即覆盖；`hosts` 是**人工设置**（优先于代码事实，导入永不覆盖）——
代码没写、写错、或「这台机器上跑得起来但代码没声明」的情况，都在集市里改。

## 三、API（服务端查询）

```bash
GET  /health
GET  /api/v1/stats                                   # 库概览（能力/策展/声明特征/导入次数/最近导入）
GET  /api/v1/capabilities?q=&group=&kind=&status=&tag=&owner=&service=&keyword=&host=&described=&conditional=&preflight=&documented=&sort=&limit=&offset=
GET  /api/v1/capabilities/{id}                       # 详情（声明/归属/能力包/策展/维护历史）
PATCH /api/v1/capabilities/{id}                      # 改集市字段 {status,owner,tags,notes,description,keywords,hosts}
GET  /api/v1/hosts                                   # 宿主注册表（适用宿主 + 各自能力数）
PATCH /api/v1/hosts/{host_id}                        # 改宿主 {display_name,kind,notes,status}
GET  /api/v1/facets                                  # group/kind/服务/宿主/状态/标签/关键字 计数
GET  /api/v1/services                                # 服务声明 + 各自能力
GET  /api/v1/imports?limit=                          # 导入历史
GET  /api/v1/events?capability_id=&limit=            # 审计流水
POST /api/v1/catalog:import                          # 导入导出器的 catalog（覆盖生成物、保留注解）
GET  /api/v1/export                                  # 库导出（含集市注解）
```

```bash
curl '127.0.0.1:4250/api/v1/capabilities?q=pdf%20页码&limit=5'
curl '127.0.0.1:4250/api/v1/capabilities?group=display&service=xiaomi.tv.display'
curl -X PATCH 127.0.0.1:4250/api/v1/capabilities/display.audio \
     -H 'Content-Type: application/json' \
     -d '{"owner":"gaolei","tags":"投屏,音频","notes":"电视出声已验证"}'
```

## 四、UI

`web/`（静态、零依赖；服务版与 GitHub Pages 版同一套代码，页头标明数据源）：

| 操作 | 说明 |
|---|---|
| 关键字 | 能力 id / 显示名 / 角色 / 触发语 / 不要派给谁 / **参数说明** / 服务 / 包 / 配置键 / **owner 与 notes**；空格 = AND |
| 分类 | `group`（32 组）/ `kind` / **服务归属** / **适用宿主** / **关键字** / 声明特征（条件挂载、有执行前自检、有文档包、组合能力、无服务归属、缺文档）/ **集市状态** |
| 详情 | 规划器识别、触发语、不要派给谁、入参出参表、**适用宿主（可点筛）**、能力描述、关键字、服务归属、条件声明、能力包、配置、文档、**集市字段编辑**、**宿主登记**、维护历史 |
| 分享 | 筛选写进 URL：`?q=电视&group=display&status=conditional` |
| 键盘 | `/` 聚焦、`Esc` 清空 |

## 五、同步与防腐烂

```bash
scripts/sync.sh /path/to/home-agent-os          # 导出 → 入库 → 回写仓库 → 自检 → 提交
scripts/sync.sh /path/to/home-agent-os --check  # CI：与代码对账（有漂移非零退出）
```

数据流：**代码 → 导出器 → 库 → `catalog/capabilities.json`（库导出，含注解）**；
`capabilities/*.md` 与 `catalog/capabilities.md` 仍是**代码视图**（随代码 PR 审阅）。
`--check` 只比声明字段（能力增删 + 契约字段），集市注解不算漂移（见 `tests/catalog-drift.py`）。

## 六、自检

```bash
python3 -m unittest discover -s server/tests -t .     # 23 个：导入/幂等/注解保留/软删恢复/描述+关键字+宿主/宿主注册表/API/socket 冒烟
node --test tests/*.test.mjs                          # 9 个：UI 查询/筛选（含关键字/宿主）/排序/高亮（纯逻辑）
python3 tests/catalog-schema.test.py                  # 目录自洽：schema/每页 md/计数/声明视图/UI 资源
python3 tests/catalog-drift.py <新导出> <仓库catalog>    # 与代码对账（CI 用）
```

## 七、部署（agent-control-plane-deployment）

- 契约：`port=4250`、`healthUrl=http://127.0.0.1:4250/health`、`startCmd/stopCmd/restartCmd = bash scripts/{start,stop,restart}.sh`；
- `build.sh`：`compileall` + 单测 + 拷进 `outputs/`（纯标准库 → 不需要 pip/venv）；
- 库在 `~/database/...`（部署 `rsync --delete` 不会碰）；`<runtime>/backend/` 放 `.env` / pid / 日志。

## 八、路线图

- 纳入 Brain 侧能力（`KNOWN_CAPABILITIES`）与其它 edge 的**声明**（同 schema，多方声明）；
- 用 `typical_triggers` 自动生成 L0 断言（忘写触发语 CI 就红）；
- 变更历史视图（按 `imports`/`events` 渲染「谁在什么时候改了什么」）；
- 提供能力包安装/分发的元数据（下载地址、版本、依赖），让集市从「登记」走到「分发」。
