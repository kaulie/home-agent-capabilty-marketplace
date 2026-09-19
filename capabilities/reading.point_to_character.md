# `reading.point_to_character`

指字认字器

kind=`action` · composition=`composite` · group=`-` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

看一张已排好的 Image Asset，识别手指指尖指向的那一个汉字，给出该字和读音。入参 asset_ref（常为 $asset_ref）。自己不拍照；现场图要先由拍照/上传步产出 Asset。不读整页文字（那是 OCR），不投屏

> 优先本能力：要认手指指的那个字时，优先本能力，不要把 decomposes_to 拆成多步，也不要用整页 OCR

## 典型触发语

- 手指指的是什么字
- 指的这个字怎么读
- 指着这个字
- 最新照片里手指指的字
- 认一下这个字
- 这个字念什么
- 这个字读啥

## 不要派给它

- 原样读图上的字
- 投屏
- 拍照本身
- 整页 OCR
- 无图知识问答
- 看图理解
- 认电视剧名

## 分解为（接线图）

- `reading.detect_finger`
- `reading.ocr_at_finger`
- `reading.rank_pointed`

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | 已排好的 Image Asset。自己不拍照。禁止 photo_url / path / 永久 URL。常为 $asset_ref。 |

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

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
