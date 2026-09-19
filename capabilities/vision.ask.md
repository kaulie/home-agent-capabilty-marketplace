# `vision.ask`

Local Vision Ask · 看图问答器

kind=`action` · composition=`atomic` · group=`vision` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

对着已经有的 Image Asset 问具体问题：照片里有几个人、电视画面在放什么。入参带用户原问句和 $asset_ref。自己不拍照；现场/电视画面要先拍再上传再问。不读小票上的字（那是 OCR），不编无图百科答案

## 典型触发语

- 图里有
- 客厅在看什么电视
- 屏幕上在放什么
- 屏幕上是什么
- 有几个人
- 有没有人
- 照片里
- 照片里有几个人
- 电视在放什么
- 电视画面里是哪部剧

## 不要派给它

- OCR
- 原样读图上的字
- 拍照本身
- 无图知识问答

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type, mime_type?}。禁止 photo_url / path / 永久 URL。常为 $asset_ref。 |
| `query` | string | 是 | 用户原话或完整问题，如「这个字读啥」「电视画面里是哪部剧」 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 针对图+问句的中文回答；不确定时直说我不知道 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.vision`

## 能力包

- `plugins/vision-ask/`

## 文档

- [home-agent-os/plugins/vision-ask/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/vision-ask/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/vision_ask.py`


- 定义层来源：`ads`、`package:vision-ask`、`service:local.vision`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
