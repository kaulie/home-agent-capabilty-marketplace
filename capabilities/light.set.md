# `light.set`

客厅大路灯 · 灯光控制器

kind=`action` · composition=`atomic` · group=`light` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

开关家里的灯（客厅大灯、台灯）：开灯、关灯、调亮一点。入参 state=on/off。不是放歌、不是念一句话假装开灯

## 典型触发语

- 亮一点
- 亮度 50
- 关台灯
- 关灯
- 台灯
- 客厅灯
- 开一下灯
- 开台灯
- 开灯
- 打开灯
- 调亮
- 调暗

## 不要派给它

- TTS
- 拍照
- 放歌

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `state` | string | 是 | on 开灯 / off 关灯；兼容 开、关、开灯、关灯 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `state` | string | 是 | 规范化后的 on 或 off |

## 适用宿主（代码事实）

- `ios`
- `mac`

## 服务声明

- `livingroom.ceiling_light`

## 能力包

- `plugins/livingroom-ceiling-light/`

## 文档

- [home-agent-os/plugins/livingroom-ceiling-light/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/livingroom-ceiling-light/capability.md)

## 入口

- ios: `ios/LivingRoomEdge/LivingRoomEdge/Light/LivingRoomLight.swift`
- mac: `mac/src/mac_edge/plugins/livingroom_light.py`

## 相关配置

- `MAC_EDGE_LIGHT_AUDIO_DIR`


- 定义层来源：`ads`、`package:livingroom-ceiling-light`、`service:livingroom.ceiling_light`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
