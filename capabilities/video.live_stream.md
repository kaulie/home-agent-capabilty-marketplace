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

（无）

## 适用宿主（代码事实）

- `mac`

## 能力包

- `plugins/video-live-stream/`

## 文档

- [home-agent-os/plugins/video-live-stream/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/video-live-stream/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/video_live_ingest.py`


- 定义层来源：`ads`、`package:video-live-stream`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
