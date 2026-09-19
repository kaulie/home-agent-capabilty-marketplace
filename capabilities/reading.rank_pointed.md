# `reading.rank_pointed`

指字排序器

kind=`action` · composition=`atomic` · group=`-` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

根据本步入参 finger 和 chars，从候选汉字里选出食指指向的那一个。入参 asset_ref + finger + chars。自己不拍照、不检测手、不做 OCR。用户要认字时不要单独排本步，用 reading.point_to_character

## 典型触发语

- 选出手指指向的字

## 不要派给它

- 投屏
- 拍照本身
- 整页 OCR
- 无图知识问答
- 检测手指

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type, mime_type?}。禁止 photo_url / path / 永久 URL。常为 $asset_ref。 |
| `chars` | array | 是 | 指尖附近 OCR 字框。由 reading.ocr_at_finger 产出。 |
| `finger` | object | 是 | 食指 {tip:[x,y], direction:[dx,dy]}。由 reading.detect_finger 产出。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 给人听/看的中文答案；认不出时直说不知道 |
| `character` | string | 是 | 指尖指向的汉字；认不出时为空串 |
| `status` | string | 否 | 引擎状态：ok / ok_with_alternatives / 其它失败状态 |

## 服务声明

- `local.character`


- 定义层来源：`ads`、`service:local.character`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
