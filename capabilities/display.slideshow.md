# `display.slideshow`

小米电视 DLNA · 多图幻灯片投屏器

kind=`output` · composition=`atomic` · group=`display` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

把多张已有 Image Asset 在电视上轮播。入参 asset_refs 数组（至少一张）。单张投屏不要用本步，不要拆成多次单图投屏

## 典型触发语

- 轮播这几张照片
- 电视上放幻灯片
- 把这些照片轮播

## 不要派给它

- 单图投屏
- 拍照
- 看图
- 按厂商选设备

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_refs` | string | 是 | 必填 AssetRef JSON 数组，至少一张。例 [{"asset_id":"asset_…","type":"image"}]。禁止 photo_urls / path / 永久 URL。不传或空数组则本能力无效。 |
| `interval_sec` | number | 否 | 每张停留秒数，默认 5 |
| `order` | string | 否 | 播放顺序，默认 array_asc：array_asc / array_desc（入参数组顺序/倒序）；alphabet_asc / alphabet_desc（按文件名）；random |

## 出参

（无）

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `xiaomi.tv.display` |

## 服务声明

- `chromecast.display`
- `xiaomi.tv.display`

## 能力包

- `plugins/chromecast-display/`
- `plugins/xiaomi-tv-display/`

## 文档

- [home-agent-os/plugins/chromecast-display/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/chromecast-display/capability.md)
- [home-agent-os/plugins/xiaomi-tv-display/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/xiaomi-tv-display/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/xiaomi_tv_display.py`

## 相关配置

- `MAC_EDGE_DISPLAY_BACKEND`
- `MAC_EDGE_XIAOMI_TV`
- `MAC_EDGE_XIAOMI_TV_HOST`
- `MAC_EDGE_XIAOMI_TV_NAME`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`package:chromecast-display`、`package:xiaomi-tv-display`、`service:chromecast.display`、`service:xiaomi.tv.display`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
