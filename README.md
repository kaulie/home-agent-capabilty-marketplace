# home-agent 能力集市（capability marketplace）

家里**所有可用能力的唯一目录**：谁提供、怎么触发、参数是什么、**此刻在不在线**。
内容由 mac edge 的代码**自动导出**（不手写），UI 支持关键字搜索 / 分类（group）/ 多维筛选。

> 🔎 打开 [`index.html`](index.html)（GitHub Pages 或本地 `python3 -m http.server`）就是可查询的界面：
> 搜能力 id、触发语、参数说明、设备名；按 group / kind / 设备 / 状态筛选；点开看完整契约。
> 人读总表：[`catalog/capabilities.md`](catalog/capabilities.md)；机器可读：[`catalog/capabilities.json`](catalog/capabilities.json)。

## 一、目录里有什么（当前快照）

| 项 | 数 | 说明 |
|---|---|---|
| 能力总数（并集） | 64 | mac edge 定义 ∪ 线上注册表 |
| 规划器广告定义（ADS） | 60 | `capability_ads.py`：kind/composition/触发语/不要派给谁 |
| 服务声明 | 44（30 个 service） | `services.py` 静态声明 + 条件声明常量 |
| 能力包 | 33 | `plugins/*/manifest.yaml`（文档 + config + entry） |
| 当前在线 | 51 | Brain `GET /api/v1/capabilities`（客厅 · Mac Edge 46 + Brain 5） |
| ⚠️ 声明未上线 | 16 | 定义有、此刻没广告（可用性门控：设备/依赖/凭证） |
| ⚠️ 线上未声明 | 4 | 在跑但不在 mac ADS 里（别的 provider：`xiaodu.*` / `map.route.estimate` / `display.audio.control`） |

「账不平」这两笔是这个仓库最直接的价值：**一眼看出「说了要做」和「真的在做」的差**。
UI 里两个状态筛选（`声明未上线` / `线上未声明`）就是它们。

## 二、每条能力长什么样（字段）

```jsonc
{
  "capability_id": "display.audio",
  "kind": "output", "composition": "atomic", "group": "display",   // 便捷字段：definition 优先、live 兜底
  "definition": {            // 代码决定的定义层（稳定；--check 只比这一层）
    "role": "音频投电视播放器",
    "planner_recognize": "把 audio Asset 交给电视 DLNA 出声…",
    "typical_triggers": ["把最新的音频在小米电视上放出来"],
    "do_not_dispatch": ["投图", "点歌放歌"],
    "input_schema": { "asset_ref": { "type": "object", "required": true, "description": "必填 AssetRef" } },
    "output_schema": { "status_text": { "type": "string", "description": "确认语" } },
    "sources": ["ads", "caps:AUDIO_DISPLAY_CAPABILITIES"]
  },
  "live": {                  // 此刻真正广告出去的契约 + 谁在线（会变）
    "role": "音频投电视播放器",
    "providers": [{ "edge_id": "edge-node-…", "edge_name": "客厅 · Mac Edge", "service_id": "xiaomi.tv.display" }]
  },
  "declared_by": ["xiaomi.tv.display"], "declared_lists": ["AUDIO_DISPLAY_CAPABILITIES"],
  "packages": ["xiaomi-tv-display"], "docs": ["plugins/xiaomi-tv-display/capability.md"],
  "entry": { "mac": "mac/src/mac_edge/plugins/xiaomi_tv_display.py" },
  "config_keys": ["MAC_EDGE_XIAOMI_TV_HOST", "…"],
  "availability": { "has_checker": false, "live": true },
  "in_ads": true, "in_live": true,
  "reconcile": { "declared_not_live": false, "live_not_declared": false, "live_differs": false }
}
```

结构约束在 [`schema/catalog.schema.json`](schema/catalog.schema.json)（由导出器生成，不会手写漂移）。

## 三、怎么维护（三条规矩）

1. **本仓库的生成物不手改**：`catalog/**`、`capabilities/**`、`schema/**` 都带「由 … 生成，请勿手改」。
   要改能力 → 改 home-agent-os（`capability_ads.py` / `services.py` / `plugins/*`）→ 跑一次同步，**diff 就是能力变更记录**。
2. **同步命令**：

   ```bash
   scripts/sync.sh /path/to/home-agent-os                          # 拉实况 + 导出 + 自检 + 提交
   scripts/sync.sh /path/to/home-agent-os --no-live --check        # CI：只对账不写入
   ```

   底层就是导出器：`python3 <home-agent-os>/mac/scripts/export_capability_catalog.py --out . --live`
3. **`--check` 不让目录腐烂**：比「代码重新导出的结果」与仓库里的 catalog（**只比定义层**：能力增删、
   契约字段、schema；实况/设备/在线状态变化不算漂移）。CI（[`.github/workflows/catalog.yml`](.github/workflows/catalog.yml)）
   每次 push 都跑自检 + 与 home-agent-os `main` 对账（对不上打 ⚠️ 不阻塞，因为能力先合在代码仓）。

## 四、UI 用法

| 操作 | 说明 |
|---|---|
| 关键字 | 搜能力 id / 显示名 / 角色 / 触发语 / **不要派给谁** / **参数说明** / 服务名 / 包名 / 配置键 / 设备名 |
| 组合查询 | 空格 = AND：`电视 音频`、`pdf 页码` |
| 分类 | `group` 下拉（32 组，按条数排序）；`kind`（input/action/output/system）；设备；状态 |
| 状态 | 在线 / **声明未上线** / **线上未声明** / 有可用性探测 / 缺文档 |
| 详情 | 点卡片：规划器识别、触发语、不要派给谁、入参/出参表、谁提供、声明归属、配置、文档链接 |
| 分享 | 所有筛选都写进 URL（`?q=电视&group=display&status=live`），可直接发链接 |
| 键盘 | `/` 聚焦搜索，`Esc` 清空 |

本地打开：`python3 -m http.server 8899` → <http://127.0.0.1:8899/>

## 五、自检

```bash
node --test tests/*.test.mjs         # 查询/筛选/排序/高亮（UI 核心逻辑）
python3 tests/catalog-schema.test.py # 目录自洽：schema、每页 md、计数、账不平标记
```

## 六、路线图

- 纳入更多提供方（Brain 侧 `KNOWN_CAPABILITIES`、其它 edge / 云）→ 同一 schema 多 provider；
- 用 `typical_triggers` **自动生成 L0 断言**（广告必须含 planner_recognize / typical_triggers / do_not_dispatch），
  能力新增忘写触发语会在 CI 红；
- 变更历史视图（每次 sync 的 diff：新增 / 移除 / 契约变化）。
