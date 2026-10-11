# `asset.inventory`

Asset 盘点查询器

kind=`system` · composition=`atomic` · group=`asset` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

查 Brain 已登记 Asset（image/video/audio/document/url 等）：今天拍了几张、第几张照片、最新 PDF/文档、最近保存的链接。问数量用 day=today/yesterday；取第 N 条用 index；最新一份用 type=document（或目标类型：链接用 type=url）+ order=newest_first + index=1，产出 asset_ref 可交给 printer.print / web.scraper 等。不是去拍照，不是翻手机相册/本机文件系统，不是看图理解

## 典型触发语

- 刚才的照片
- 我今天拍了几张照片
- 把最新的PDF打印出来
- 把最新的文件打印出来
- 昨天拍了多少张照片
- 最后一张照片
- 最新的PDF
- 最新的文件
- 最近有哪些图
- 看下最新的pdf文档
- 给我看第五张照片

## 不要派给它

- 手机系统相册
- 扫本机磁盘
- 投屏
- 拍照
- 看图理解

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `day` | string | 否 | today / yesterday / YYYY-MM-DD；问昨天拍了几张填 yesterday |
| `include_refs` | string | 否 | true/false，是否产出 asset_refs |
| `index` | number | 否 | 1 起取第 N 条；最新一份配合 order=newest_first 填 1 |
| `limit` | number | 否 | 返回 asset_refs 上限，默认 50 |
| `offset` | number | 否 | 跳过前 N 条（0 起）；与 index 二选一，优先 index |
| `order` | string | 否 | newest_first（默认列表/取最新）或 oldest_first（index 默认） |
| `producer_capability` | string | 否 | 只统计该生产者产出的 Asset（可选过滤） |
| `since` | string | 否 | 起始时间 ISO 或 unix |
| `timezone` | string | 否 | IANA 时区，默认 Asia/Shanghai |
| `type` | string | 否 | asset 类型：image / video / audio / document / url 等；最新 PDF 填 document、保存的链接填 url |
| `until` | string | 否 | 结束时间 ISO 或 unix（不含） |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 中文盘点结果 |
| `asset_ref` | string | 否 | 单条 AssetRef（index 或仅一条时）；打印可交给 printer.print |
| `asset_refs` | string | 否 | AssetRef JSON 数组 |
| `count` | string | 是 | 匹配数量 |

## 适用宿主（代码事实）

- `brain`

## 服务声明

- `system.asset`

## 能力包

- `plugins/asset-inventory/`

## 文档

- [plugins/asset-inventory/capability.md](../plugins/asset-inventory/capability.md)


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `c272647`），请勿手改。</sub>
