# `display.pdf`

PDF 投屏（逐页渲染） · PDF 投屏打开器

kind=`output` · composition=`atomic` · group=`display` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把本步已有的 PDF/document Asset 投到电视上显示（每页渲染成图片逐页投）。入参 asset_ref（必填，type=document，常为 $asset_ref），可选 page（默认第 1 页）。用户没指定哪份 PDF 时，先排 asset.inventory 取最新 document 再接本步。本步只打开并显示，翻页用 display.pdf.page；不打印、不 OCR、不看图理解

## 典型触发语

- PDF 上电视
- 把最新的 PDF 投屏到电视上
- 把这个文档投到电视上看
- 把这份 PDF 投到电视

## 不要派给它

- OCR
- 下一页
- 单图投屏
- 幻灯片
- 打印
- 看图理解
- 翻页

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type, mime_type?}，type 必须为 document（PDF）。禁止 path / 永久 URL。常为 $asset_ref。 |
| `page` | number | 否 | 打开后显示的页码（1-based），默认第 1 页 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `page` | number | 是 | 当前投屏页码（1-based） |
| `page_count` | number | 是 | PDF 总页数 |
| `status_text` | string | 是 | 中文一句话，如「已把 PDF 投到电视，第 1 页 / 共 12 页」 |

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
