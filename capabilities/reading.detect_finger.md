# `reading.detect_finger`

食指检测器

kind=`action` · composition=`atomic` · group=`-` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

看一张已有 Image Asset，找出食指指尖位置和指向。入参 asset_ref。自己不拍照、不认字、不 OCR。用户要认手指指的字时不要单独排本步，用 reading.point_to_character

## 典型触发语

- 指尖在哪
- 检测图里的食指

## 不要派给它

- 投屏
- 拍照本身
- 整页 OCR
- 无图知识问答
- 认字

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type, mime_type?}。手指指向某字的图片。禁止 photo_url / path / 永久 URL。常为 $asset_ref。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `finger` | object | 是 | 食指 {tip:[x,y], direction:[dx,dy]} |
| `status` | string | 否 | 引擎状态 |

## 服务声明

- `local.character`


- 定义层来源：`ads`、`service:local.character`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
