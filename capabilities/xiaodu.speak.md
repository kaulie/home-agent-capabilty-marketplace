# `xiaodu.speak`

小度音箱 · 小度音箱播报器

kind=`output` · composition=`atomic` · group=`notify` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把指定文案经客厅小度音箱播报出来。入参 text=要念的那句话。用户明确说「用小度说/播报」时用本步，不要用 Mac 本机 notify.speak

## 典型触发语

- 客厅音箱说
- 小度播报
- 小度音箱播报
- 用小度说
- 让小度念

## 不要派给它

- Mac 本机播报
- 回读上一步答案
- 投屏
- 放歌
- 知识问答

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `text` | string | 是 | 要经小度音箱播报的原文 |
| `voice` | string | 否 | edge-tts 音色，默认 zh-CN-XiaoxiaoNeural |

## 出参

（无）

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `xiaodu.speaker`

## 能力包

- `plugins/xiaodu-speaker/`

## 文档

- [home-agent-os/plugins/xiaodu-speaker/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/xiaodu-speaker/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/xiaodu_speaker.py`


- 定义层来源：`ads`、`package:xiaodu-speaker`、`service:xiaodu.speaker`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
