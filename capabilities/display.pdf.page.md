# `display.pdf.page`

PDF 投屏（逐页渲染） · PDF 投屏翻页器

kind=`output` · composition=`atomic` · group=`display` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

电视正在投屏 PDF 时翻页：下一页（默认）/上一页/翻到第 N 页。入参 action=next/prev/goto（goto 必填 page）。不需要 asset_ref——翻的是当前投屏会话里那份 PDF。没有正在投屏的 PDF 时本步会失败，应先经 display.pdf 打开会话

## 典型触发语

- 上一页
- 下一页
- 往前翻
- 往后翻
- 翻到第 5 页
- 翻页

## 不要派给它

- 切歌
- 单图投屏
- 打印
- 打开 PDF
- 投屏新文档
- 看图理解

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `action` | string | 否 | next（默认）/ prev / goto；也接受 下一页/上一页/翻到 等中文 |
| `page` | number | 否 | action=goto 时必填的目标页码（1-based） |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `page` | number | 是 | 翻页后当前页码（1-based） |
| `page_count` | number | 是 | PDF 总页数 |
| `status_text` | string | 是 | 中文一句话，如「已翻到第 2 页 / 共 12 页」 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `chromecast.display`
- `xiaomi.tv.display`

## 条件声明

- `PDF_DISPLAY_CAPABILITIES`（按依赖/后端决定是否挂上）

## 能力包

- `plugins/pdf-display/`

## 文档

- [home-agent-os/plugins/pdf-display/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/pdf-display/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/pdf_display.py`

## 相关配置

- `MAC_EDGE_DISPLAY_BACKEND`
- `MAC_EDGE_PDF_DISPLAY_DPI`
- `MAC_EDGE_XIAOMI_TV_HOST`


- 定义层来源：`ads`、`caps:PDF_DISPLAY_CAPABILITIES`、`package:pdf-display`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
