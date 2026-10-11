# `image.ocr`

图片文字识别器

kind=`system` · composition=`atomic` · group=`ocr` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

读已有 Image Asset 上整页/整段印着的字（小票、说明书、手写），原样吐出文字和坐标，不解释、不总结、不教识字。入参必须是 asset_ref。自己不拍照。手指指的单个字不要用本步，用 reading.point_to_character

## 典型触发语

- OCR
- 图上写了什么
- 把小票上的字读出来
- 识别照片里的字
- 说明书上印的字

## 不要派给它

- 手指指的字
- 拍照本身
- 指字认字
- 搜图
- 文档总结
- 文生图
- 看图理解
- 看图问答
- 识字教学
- 这个字念什么
- 这个字读啥

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | 图片 AssetRef JSON {asset_id, type}。禁止 image_url / path / base64。 |
| `language` | string | 否 | zh（默认）或 en |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_id` | string | 是 | 入参图片 asset_id |
| `blocks` | string | 是 | OCR 块 JSON 数组 |
| `text` | string | 是 | 图上全部识别文字 |

## 适用宿主（代码事实）

- `brain`

## 服务声明

- `system.ocr`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `c272647`），请勿手改。</sub>
