# `image.ocr`

图片文字识别器

kind=`system` · composition=`atomic` · group=`ocr` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

读已有 Image Asset 上整页/整段印着的字（小票、说明书、手写），原样吐出文字和坐标，不解释、不总结、不教识字。入参必须是 asset_ref。自己不拍照。手指指的单个字不要用本步，用 reading.point_to_character

## 典型触发语

- 图上写了什么
- 识别照片里的字
- OCR
- 把小票上的字读出来
- 说明书上印的字

## 不要派给它

- 看图理解
- 看图问答
- 文档总结
- 识字教学
- 拍照本身
- 搜图
- 文生图
- 手指指的字
- 这个字读啥
- 这个字念什么
- 指字认字

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | 图片 AssetRef JSON {asset_id, type, mime_type?} 或 asset_id。禁止 image_url / path / base64。 |
| `language` | string | 否 | zh（默认）或 en |
| `return_bbox` | string | 否 | 是否返回 bbox，默认 true |
| `return_confidence` | string | 否 | 是否返回 confidence，默认 true |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_id` | string | 是 | 入参图片的 asset_id |
| `blocks` | string | 是 | OCR 块 JSON 数组 [{text, bbox, confidence}] |
| `engine` | string | 否 | OCR 引擎名（如 paddleocr），不是能力 id |
| `language` | string | 否 | 识别语言 |
| `model` | string | 否 | 模型名 |
| `model_version` | string | 否 | 模型版本 |
| `text` | string | 是 | 图上全部识别文字（原样拼接，不做理解） |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| Brain | `system` | `system.ocr` |

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
