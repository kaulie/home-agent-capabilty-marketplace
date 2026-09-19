# `camera.capture`

GoPro Camera · 拍照执行器

kind=`input` · composition=`atomic` · group=`camera` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

按快门拍一张现场照（客厅、电视画面、眼前的东西），写入本机 inbox，产出 capture_ref（还不是 Asset）。允许当「给人看 / 问图上有什么 / 投电视」的前序步。本步不上传、不投屏、不能单步当最终图。下一步上传用 $capture_ref。禁止把 path 写进 plan

## 典型触发语

- 拍一下
- 拍一下电视屏幕
- 拍一张
- 拍张照
- 拍照
- 拍的照片
- 看看客厅电视画面
- 看看现在

## 不要派给它

- 上传
- 传到云上
- 传到图床
- 单步作为最终给用户看的图
- 放歌
- 无拍照直接回答画面内容

## 入参

（无）

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `capture_ref` | string | 是 | CaptureRef JSON {capture_id, type, mime_type}。本机 inbox 句柄，还不是 Asset。禁止 path / photo_url / asset_id。 |

## 适用宿主（代码事实）

- `ios`
- `python`

## 服务声明

- `gopro.camera`

## 能力包

- `plugins/gopro-camera/`

## 文档

- [home-agent-os/plugins/gopro-camera/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/gopro-camera/capability.md)

## 入口

- ios: `ios/GoProPluginEntry.swift`
- python: `driver.py`


- 定义层来源：`ads`、`package:gopro-camera`、`service:gopro.camera`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
