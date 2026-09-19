# `file.convert`

文件格式转换器 · 文件格式转换器

kind=`action` · composition=`atomic` · group=`convert` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把本步已有的一张或多张 Image Asset 按顺序合并转成一个 PDF 文档 Asset。入参 asset_refs（必填，type=image 数组，顺序即页码）、to_format=pdf（可选 from_format=image）。本能力只产出 PDF，不打印、不 OCR、不识别内容

## 典型触发语

- 合成一个 PDF
- 图片转 PDF
- 把扫描件导成 PDF
- 把这几张图转成 PDF
- 把这几张照片合并成 PDF
- 转成 PDF 文件

## 不要派给它

- OCR
- 图片上传本身
- 打印
- 投屏
- 拍照
- 文字识别
- 看图理解

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_refs` | string | 是 | 必填 AssetRef JSON 数组，至少一张，type 必须为 image（JPEG/PNG）。数组顺序 = PDF 页码顺序。例 [{"asset_id":"asset_…","type":"image"}]。禁止 path / 永久 URL / base64。 |
| `from_format` | string | 否 | 源格式；缺省按 asset_refs 类型推断为 image。显式传非 image 则明确失败。 |
| `name` | string | 否 | 可选生成的 PDF 展示名（不含或自动补 .pdf）；不传则用 convert-<时间戳>.pdf。 |
| `to_format` | string | 是 | 目标格式；一期仅接受 pdf，其它值明确失败。例 "pdf"。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 新登记 document（PDF）Asset 的 AssetRef JSON |
| `page_count` | number | 是 | PDF 页数（= 图片数） |
| `status_text` | string | 是 | 中文一句话结果，含页数与 asset_id |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.file.convert`

## 能力包

- `plugins/file-convert/`

## 文档

- [home-agent-os/plugins/file-convert/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/file-convert/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/file_convert.py`


- 定义层来源：`ads`、`package:file-convert`、`service:local.file.convert`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
