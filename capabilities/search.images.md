# `search.images`

Web Image Search · 互联网实拍图检索器

kind=`action` · composition=`atomic` · group=`search` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

按关键词去网上搜存量实拍图（必应/Openverse），例如「搜一张故宫的照片」「找几张风景图」。不是 AI 画图，不是拍家里，不是翻本机相册。产出 asset_refs。投电视要另排投屏步

## 典型触发语

- 搜一张猫的照片
- 找网上的实拍图
- 搜索故宫的照片
- 给我找几张风景图
- 网上搜几张实拍

## 不要派给它

- AI文生图
- 画一张
- 生成图片
- 知识问答
- 拍照
- 看本地相册
- 投屏本身
- OCR
- 读图上的字

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `count` | string | 否 | 返回张数 1–8，默认 4 |
| `freshness` | string | 否 | 可选时效（Bing）：Day / Week / Month |
| `provider` | string | 否 | 搜图源 bing \| openverse。缺省：环境变量，否则有密钥用 Bing，否则 Openverse |
| `query` | string | 是 | 搜索关键词。检索网上存量实拍图，不是 AI 生图。 |
| `size` | string | 否 | 可选尺寸（Bing）：Small / Medium / Large / Wallpaper |
| `upload_dest` | string | 否 | 登记图床目标 lan（默认）\| cloud |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_refs` | string | 是 | AssetRef JSON 数组，至少一张。禁止 photo_url / path / 永久 URL。 |
| `hit_count` | string | 是 | 成功登记的张数 |
| `provider` | string | 否 | 实际使用的搜图源 bing \| openverse |
| `query_used` | string | 是 | 实际搜索关键词 |
| `sources` | string | 否 | 来源页 JSON 数组 [{name, host_page, license?}] |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `local.search` |

## 服务声明

- `local.search`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`service:local.search`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
