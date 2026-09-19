# `pdf.to_images`

PDF 页面渲染器 · PDF 页面渲染器

kind=`action` · composition=`atomic` · group=`convert` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把本步已有的 PDF/document Asset 的每页（或 page_start–page_end 页范围）渲染成高清 PNG 图片并逐页登记为 image Asset，产出 asset_refs（顺序=页码），可交给 display.slideshow 轮播、逐页 OCR、vision.ask 看某页等下游。入参 asset_ref（必填，type=document），可选 page_start/page_end/dpi（默认 200）。本能力只渲染登记图片，不投屏、不 OCR、不打印；电视翻页场景用 display.pdf，不要经本能力整份预渲染

## 典型触发语

- PDF 转图片
- 把 PDF 第 3 到 5 页转成图
- 把这个 PDF 每页转成图片
- 把这份 PDF 拆成一页一页的图

## 不要派给它

- OCR
- PDF 旋转
- 图片合成 PDF
- 打印
- 投屏翻页
- 拍照
- 看图理解

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 必填 AssetRef JSON，type=document（PDF）。例 {"asset_id":"asset_…","type":"document"}。禁止 path / 永久 URL；缺则本能力无效。 |
| `dpi` | number | 否 | 渲染清晰度 DPI，默认 200（钳制 72–400） |
| `name` | string | 否 | 可选页图文件名前缀；不传则用 pdf-<asset_id 前 12 位> |
| `page_end` | number | 否 | 结束页（1-based，闭区间），缺省最后一页；越界钳到边界 |
| `page_start` | number | 否 | 起始页（1-based），缺省第 1 页；越界钳到边界 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_refs` | string | 是 | 页图 AssetRef JSON 数组，顺序=页码。可交给 display.slideshow / OCR / vision 等下游。 |
| `page_count` | number | 是 | PDF 总页数 |
| `rendered_pages` | number | 是 | 本次实际渲染页数 |
| `status_text` | string | 是 | 中文一句话结果，含页范围、页数与 DPI |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.pdf.images`

## 能力包

- `plugins/pdf-to-images/`

## 文档

- [home-agent-os/plugins/pdf-to-images/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/pdf-to-images/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/pdf_to_images.py`

## 相关配置

- `MAC_EDGE_PDF_DISPLAY_DPI`


- 定义层来源：`ads`、`package:pdf-to-images`、`service:local.pdf.images`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
