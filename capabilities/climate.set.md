# `climate.set`

客厅海信空调 · 空调控制器

kind=`action` · composition=`atomic` · group=`climate` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

控制绑定的空调：开/关、制冷/制热/送风、设定 16–32 度、风速、左右/上下扫风。多台时用 appliance 显示名区分客厅空调/儿童房空调。不做新风、不做除湿、不开灯

## 典型触发语

- 关掉空调
- 制冷 26 度
- 制热
- 左右扫风
- 打开空调
- 空调调到二十六度
- 风速高

## 不要派给它

- TTS
- 开灯
- 放歌
- 新风
- 知识问答
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

## 适用宿主（代码事实）

- `mac`

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


- 定义层来源：`ads`、`package:hisense-ac`、`service:livingroom.climate`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
