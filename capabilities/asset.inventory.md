# `asset.inventory`

Asset 盘点查询器

kind=`system` · composition=`atomic` · group=`asset` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

查 Brain 已登记 Asset（image/video/audio/document/url 等）：今天拍了几张、第几张照片、最新 PDF/文档、最近保存的链接。问数量用 day=today/yesterday；取第 N 条用 index；最新一份用 type=document（或目标类型：链接用 type=url）+ order=newest_first + index=1，产出 asset_ref 可交给 printer.print / web.scraper 等。不是去拍照，不是翻手机相册/本机文件系统，不是看图理解

## 典型触发语

- 我今天拍了几张照片
- 昨天拍了多少张照片
- 最近有哪些图
- 刚才的照片
- 最后一张照片
- 给我看第五张照片
- 最新的PDF
- 最新的文件
- 看下最新的pdf文档
- 把最新的PDF打印出来
- 把最新的文件打印出来

## 不要派给它

- 拍照
- 看图理解
- 投屏
- 手机系统相册
- 扫本机磁盘

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `day` | string | 否 | today / yesterday / YYYY-MM-DD；问「今天拍了几张」填 today，「昨天」填 yesterday |
| `include_refs` | string | 否 | true/false，是否产出 asset_refs；只要数量可 false |
| `index` | number | 否 | 1 起：按登记时间取第 N 条（默认 oldest_first）；看「第五张」填 5；最新一份配合 order=newest_first 填 1 |
| `limit` | number | 否 | 返回 asset_refs 上限，默认 50；取第 N 张时用 index，不要用 limit=N |
| `offset` | number | 否 | 跳过前 N 条（0 起）；与 index 二选一，优先 index |
| `order` | string | 否 | newest_first（默认列表/取最新）或 oldest_first（index 默认） |
| `producer_capability` | string | 否 | 只统计该生产者产出的 Asset（可选过滤；填生产者标识，不要在口语里念给用户） |
| `since` | string | 否 | 起始时间 ISO 或 unix；与 day 二选一优先 day |
| `timezone` | string | 否 | IANA 时区，默认 Asia/Shanghai |
| `type` | string | 否 | asset 类型：image / video / audio / document 等；问照片填 image，最新 PDF/文档填 document |
| `until` | string | 否 | 结束时间 ISO 或 unix（不含） |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 中文盘点结果，如「今天一共登记了 12 张照片。」；取第 N 张时为定位说明 |
| `asset_ref` | object | 否 | 单张 AssetRef（index 或仅一条时） |
| `asset_refs` | string | 否 | AssetRef JSON 数组（include_refs 时） |
| `count` | string | 是 | 匹配数量 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| Brain | `system` | `system.asset` |

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
