# `xiaodu.speak`

小度音箱 · 小度音箱播报器

kind=`output` · composition=`atomic` · group=`notify` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

把指定文案经客厅小度音箱播报出来。入参 text=要念的那句话。用户明确说「用小度说/播报」时用本步，不要用 Mac 本机 notify.speak

## 典型触发语

- 用小度说
- 小度播报
- 客厅音箱说
- 让小度念
- 小度音箱播报

## 不要派给它

- Mac 本机播报
- 知识问答
- 放歌
- 投屏
- 回读上一步答案

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `text` | string | 是 | 要经小度音箱播报的原文 |
| `voice` | string | 否 | edge-tts 音色，默认 zh-CN-XiaoxiaoNeural |

## 出参

（无）

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `xiaodu.speaker` |

## 服务声明

- `xiaodu.speaker`

## 能力包

- `plugins/xiaodu-speaker/`

## 文档

- [home-agent-os/plugins/xiaodu-speaker/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/xiaodu-speaker/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/xiaodu_speaker.py`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`package:xiaodu-speaker`、`service:xiaodu.speaker`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
