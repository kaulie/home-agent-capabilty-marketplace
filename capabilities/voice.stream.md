# `voice.stream`

Local Voice Stream · 常驻语音流入口

kind=`input` · composition=`atomic` · group=`voice` · 声明=`是` · 在线=`是`

## 规划器怎么认它

客厅/手机上一直开着的麦克风：自己收音、转写，把口语变成意图。这是常驻入口，不是用户任务里的一步，不要排进 plan

## 典型触发语

- 对着麦克风说话
- 语音下指令

## 不要派给它

- 作为计划逐步执行
- 知识问答
- 控制设备
- 投屏

## 入参

（无）

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `transcript` | string | 否 | 最近一次转写（观测用；常驻入口不经计划逐步产出） |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `local.voice` |

## 服务声明

- `local.voice`

## 能力包

- `plugins/voice-stream/`

## 文档

- [home-agent-os/plugins/voice-stream/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/voice-stream/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/voice_stream.py`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`package:voice-stream`、`service:local.voice`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
