# `pdf.rotate`

PDF 旋转器 · PDF 旋转器（横版/竖版）

kind=`action` · composition=`atomic` · group=`convert` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

把本步已有的 PDF/document Asset 整份转成横版或竖版（先判断当前是横版还是竖版，需要旋转的页转 90°）。入参 asset_ref（必填，type=document）、orientation（必填，portrait=竖版 / landscape=横版，可写中文）。产出新的document Asset 或无需旋转时复用原 asset_ref。转完通常交给 printer.print 打印

## 典型触发语

- 把这个 PDF 转成横版
- 把这个 PDF 转成竖版
- 横着打这份 PDF
- 竖着打这份 PDF
- 把 PDF 旋转成横版
- PDF 横竖切换

## 不要派给它

- 打印
- OCR
- 看图理解
- 扫描
- 识别内容
- PDF 合成/转图片
- 配网

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 必填 AssetRef JSON，type=document（PDF）。例 {"asset_id":"asset_…","type":"document"}。禁止 path / 永久 URL；缺则本能力无效。 |
| `name` | string | 否 | 可选生成的 PDF 展示名（不含或自动补 .pdf）；不传则用 pdf-rotate-<时间戳>-<横版\|竖版>.pdf。 |
| `orientation` | string | 是 | 目标方向：portrait=竖版 / landscape=横版；也接受 竖版/横版/竖向/横向 等中文别名。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 旋转后新登记 document AssetRef；无需旋转时为原 asset_ref |
| `page_count` | number | 是 | PDF 页数 |
| `rotated_pages` | number | 是 | 实际旋转 90° 的页数（0=无需旋转，复用原 asset） |
| `source_orientation` | string | 是 | 整份判出的原始方向：portrait / landscape / mixed / square |
| `status_text` | string | 是 | 中文一句话结果，含页数、方向与 asset_id |
| `target_orientation` | string | 是 | 请求的目标方向：portrait / landscape |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `local.pdf.rotate` |

## 服务声明

- `local.pdf.rotate`

## 能力包

- `plugins/pdf-rotate/`

## 文档

- [home-agent-os/plugins/pdf-rotate/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/pdf-rotate/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/pdf_rotate.py`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`package:pdf-rotate`、`service:local.pdf.rotate`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
