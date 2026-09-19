# `reading.ocr_at_finger`

指尖附近文字识别器

kind=`action` · composition=`atomic` · group=`-` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

在已有 Image Asset 上，按本步入参 finger 裁指尖附近窗口做 OCR，产出字框。入参 asset_ref + finger。不是整页 OCR（那是 image.ocr）。用户要认指向的那个字时不要单独排本步，用 reading.point_to_character

## 典型触发语

- 识别指尖附近的字

## 不要派给它

- 投屏
- 拍照本身
- 整页 OCR
- 无图知识问答
- 看图理解

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type, mime_type?}。禁止 photo_url / path / 永久 URL。常为 $asset_ref。 |
| `finger` | object | 是 | 食指 {tip:[x,y], direction:[dx,dy]}。由 reading.detect_finger 产出。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `chars` | array | 是 | 指尖附近 OCR 字框列表 |
| `status` | string | 否 | 引擎状态 |

## 服务声明

- `local.character`


- 定义层来源：`ads`、`service:local.character`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
