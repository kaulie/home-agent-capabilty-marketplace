# `display.pdf.page`

小米电视 DLNA · PDF 投屏翻页器

kind=`output` · composition=`atomic` · group=`display` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

电视正在投屏 PDF 时翻页：下一页（默认）/上一页/翻到第 N 页。入参 action=next/prev/goto（goto 必填 page）。不需要 asset_ref——翻的是当前投屏会话里那份 PDF。没有正在投屏的 PDF 时本步会失败，应先经 display.pdf 打开会话

## 典型触发语

- 下一页
- 上一页
- 翻到第 5 页
- 翻页
- 往后翻
- 往前翻

## 不要派给它

- 打开 PDF
- 投屏新文档
- 打印
- 看图理解
- 切歌
- 单图投屏

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

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `xiaomi.tv.display` |

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

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`caps:PDF_DISPLAY_CAPABILITIES`、`package:pdf-display`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
