# `climate.set`

主卧空调 · 主卧空调控制器

kind=`action` · composition=`atomic` · group=`climate` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

控制「主卧空调」：开关、制冷/制热/送风、设定温度、风速、扫风。仅当用户点名该设备时使用本实例，不要派给其它同 capability 的在线节点。

## 典型触发语

- 打开主卧空调
- 关掉主卧空调
- 关闭主卧空调
- 开主卧空调
- 关主卧空调
- 打开空调
- 关掉空调
- 制冷 26 度
- 风速高
- 左右扫风
- 制热
- 空调调到二十六度

## 不要派给它

- 放歌
- TTS
- 开灯
- 知识问答
- 新风
- 除湿

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `appliance` | string | 否 | 绑定空调的显示名，如 客厅空调、儿童房空调。本机绑定多台时必填。 |
| `fan` | string | 否 | auto 自动 / diffuse 柔风 / low 低 / medium 中 / high 高。未写 power 时本步内部先开机。 |
| `mode` | string | 否 | cool 制冷 / heat 制热 / fan 送风。未写 power 时本步内部先开机。 |
| `power` | string | 否 | on 开 / off 关（兼容 开、关、打开、关闭）。与 mode、target_temp、fan、swing 至少填一项。off 时不可同时设模式、温度、风速或扫风。 |
| `swing` | string | 否 | off 关 / on 开 / horizontal 左右 / vertical 上下。未写 power 时本步内部先开机。 |
| `target_temp` | number | 否 | 设定温度，摄氏整数 16–32。送风模式不可设温。未写 power 时本步内部先开机。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fan` | string | 否 | auto / diffuse / low / medium / high |
| `indoor_temp` | number | 否 | 室内温度 |
| `mode` | string | 是 | cool / heat / fan / dry / auto |
| `power` | string | 是 | 规范化后的 on 或 off |
| `status_text` | string | 是 | 人类可读状态，如「空调已开，制冷 26°C，风速中，左右扫风」 |
| `swing` | string | 否 | off / on / horizontal / vertical |
| `target_temp` | number | 否 | 当前设定温度 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `climate.39835afb10` |
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `climate.d0034cdb00` |
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `climate.kids_room` |
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `climate.living_room` |

## 服务声明

- `livingroom.climate`

## 能力包

- `plugins/hisense-ac/`

## 文档

- [home-agent-os/plugins/hisense-ac/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/hisense-ac/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/hisense_ac.py`

## 相关配置

- `MAC_EDGE_HISENSE_DEVICE_ID`
- `MAC_EDGE_HISENSE_HOME_ID`
- `MAC_EDGE_HISENSE_PASSWORD`
- `MAC_EDGE_HISENSE_USERNAME`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`package:hisense-ac`、`service:livingroom.climate`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
