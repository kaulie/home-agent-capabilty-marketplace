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

（无）

## 出参

（无）

## 适用宿主（代码事实）

- `brain`

## 能力包

- `plugins/asset-inventory/`

## 文档

- [home-agent-os/plugins/asset-inventory/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/asset-inventory/capability.md)


- 定义层来源：`ads`、`package:asset-inventory`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
