# 服务架构

## 数据流

```
plugins/ + declarations/
        │  scripts/export_catalog.py
        ▼
  导出 catalog（声明字段；decomposes_to 保序）
        │  POST /api/v1/catalog:import 或 scripts/sync.sh
        ▼
  SQLite marketplace.sqlite3
        │
        ├─ GET /api/v1/export          → Brain / Gateway
        ├─ GET/PATCH /api/v1/capabilities → UI 注解
        └─ 回写 catalog/capabilities.json（含注解，给 git 对账）
```

权威源是本仓 `plugins/` + `declarations/`。不读 home-agent-os / brain / gateway。

## HTTP 面（完整表以 README 与 `server/` 为准）

| 路径 | 作用 |
|---|---|
| `GET /health` | 探活 |
| `GET /api/v1/export` | **规划器契约**：含集市注解的库导出 |
| `GET /api/v1/capabilities` | 筛选列表 |
| `PATCH /api/v1/capabilities/{id}` | 只改集市字段 |
| `POST /api/v1/catalog:import` | 导入：覆盖生成物、保留注解 |
| `GET /api/v1/hosts` / `PATCH ...` | 宿主注册表 |
| `GET /api/v1/stats` / `facets` / `imports` / `events` | 概览与审计 |

## 两套字段

| 层 | 例子 | 导入时 |
|---|---|---|
| 生成物（代码事实） | kind、role、触发语、schema、`runs_on`、`decomposes_to` | **覆盖** |
| 集市（人） | status、owner、tags、notes、description、keywords、`hosts` | **永不覆盖** |

`runs_on` 来自 `plugins/*/manifest.yaml` 的 `platforms:` / `entry:`（如 `mac` / `brain` / `ios` / `android`）。`hosts` 是人工设置，优先于代码事实。

软删：代码里消失的能力 `in_catalog=0`，注解留下，代码回来即恢复。

## 存储

生产库：`~/database/home-agent-capability-marketplace/marketplace.sqlite3`（代码与 runtime 之外）。部署 rsync **不应**碰它。

## 外部依赖

无强制三方运行时。Brain / Gateway 是本服务的**读方**，本进程不调它们生成目录。
