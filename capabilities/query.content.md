# `query.content`

Local Query · 文本知识与推理回答器

kind=`action` · composition=`atomic` · group=`query` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

家里没有对应设备能力时，用文本回答百科/讲解/应用题（为什么天是蓝的、这道题怎么解）。不要当钟、不要看家里的图、不要介绍你会什么、不要投电视。仅当用户明确说「画一张/生成一张图」才走本步生图（AI 文生图，不是搜网上实拍）；生图成功才有 asset_ref

## 典型触发语

- 为什么天是蓝的
- 帮我解释一下
- 来张战斗机的图片
- 生成一张示意图
- 画一只猫
- 这道应用题怎么解

## 不要派给它

- OCR
- Openverse检索
- 今天几号
- 你会什么
- 你会开
- 你可以做什么
- 你可以控制
- 墙上几点
- 必应检索
- 找真实照片
- 把这张图投到电视
- 投屏
- 报时
- 拍照
- 控制设备
- 搜网上实拍图
- 文搜图
- 现在几点了
- 看图
- 能力介绍
- 读图上的字
- 资产盘点
- 闲聊问候

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `query` | string | 是 | 用户原话 / prompt。出图投屏时请保留「来张图/投电视」等语义，不要只塞主题词。 |
| `upload_dest` | string | 否 | 生图上传目标 lan（默认）\| cloud |
| `want_image` | string | 否 | true 时本步必须生图并产出 asset_ref（planner 在出图/投屏计划里可显式传）。缺省则看 query 是否含来张/图片/投屏等。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 文字答案；不确定时直说我不知道 |
| `asset_ref` | string | 否 | 仅生图成功时的 AssetRef JSON {asset_id, type, mime_type?}。禁止 photo_url / path / 永久 URL。 |
| `citations` | string | 否 | 来源 JSON 数组；拒答时为 [] |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.query`

## 能力包

- `plugins/query-content/`

## 文档

- [home-agent-os/plugins/query-content/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/query-content/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/query_content.py`


- 定义层来源：`ads`、`package:query-content`、`service:local.query`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
