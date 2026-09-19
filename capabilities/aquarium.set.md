# `aquarium.set`

米家智能鱼缸 · 鱼缸控制器

kind=`action` · composition=`atomic` · group=`aquarium` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

控制米家鱼缸：喂鱼、开关缸/灯/水泵、调流量。问水温也走本步读状态。不开锁、不开空调

## 典型触发语

- 关鱼缸
- 喂鱼
- 开鱼缸灯
- 给鱼喂一口
- 鱼缸水温

## 不要派给它

- TTS
- 开空调
- 开锁
- 投屏
- 知识问答

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `feed` | string | 否 | true 或 1–10：立即喂一份或指定份数 |
| `light` | string | 否 | on 开灯 / off 关灯 |
| `power` | string | 否 | on 开 / off 关（兼容 开、关、打开、关闭）。与 light、pump、pump_flux、feed 至少填一项。 |
| `pump` | string | 否 | on 开水泵 / off 关水泵 |
| `pump_flux` | number | 否 | 水泵流量 1–10 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `fed` | boolean | 否 | 本步是否已喂食 |
| `light` | string | 否 | on / off |
| `power` | string | 否 | on / off |
| `pump` | string | 否 | on / off |
| `pump_flux` | number | 否 | 当前水泵流量 |
| `status_text` | string | 是 | 人类可读状态，如「鱼缸已开，灯开，水温26°C」 |
| `water_temp` | number | 否 | 水温摄氏 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `livingroom.aquarium`

## 能力包

- `plugins/xiaomi-aquarium/`

## 文档

- [home-agent-os/plugins/xiaomi-aquarium/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/xiaomi-aquarium/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/xiaomi_aquarium.py`

## 相关配置

- `MAC_EDGE_XIAOMI_AQUARIUM_DID`
- `MAC_EDGE_XIAOMI_COUNTRY`
- `MAC_EDGE_XIAOMI_PASSWORD`
- `MAC_EDGE_XIAOMI_USERNAME`


- 定义层来源：`ads`、`package:xiaomi-aquarium`、`service:livingroom.aquarium`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
