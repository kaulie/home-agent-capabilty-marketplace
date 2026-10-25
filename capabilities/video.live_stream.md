# `video.live_stream`

Video Live Stream · iPhone 实时视频流入口

kind=`input` · composition=`atomic` · group=`video` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把 iPhone 摄像头编成实时视频流推到 Mac。常驻推流，不是拍一张、不是看图问答、不要当 plan 逐步执行

## 典型触发语

- 开始直播
- 推摄像头画面

## 不要派给它

- 作为计划逐步执行
- 投屏
- 抽帧上传
- 看图理解

## 入参

（无）

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `stream_id` | string | 否 | 本次推流 id（观测用；常驻入口不经计划逐步产出） |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `iphone.video`

## 能力包

- `plugins/video-live-stream/`

## 文档

- [plugins/video-live-stream/capability.md](../plugins/video-live-stream/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/video_live_ingest.py`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `62e850e`），请勿手改。</sub>
