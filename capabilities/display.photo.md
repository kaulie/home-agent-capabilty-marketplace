# `display.photo`

小米电视 DLNA · 单图投屏器

kind=`output` · composition=`atomic` · group=`display` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把一张已有 Image Asset 投到电视/投屏端。入参 asset_ref（常为 $asset_ref）。这是计划步，不能只用 presentation.endpoint 代替。多张轮播不要用本步

## 典型触发语

- 丢到电视
- 把这张图投到电视
- 投到电视
- 投屏
- 放到电视

## 不要派给它

- 幻灯片
- 拍多图
- 按厂商选 Chromecast
- 放歌

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type, mime_type?}。禁止 photo_url / path / 永久 URL。常为 $asset_ref。 |

## 出参

（无）

## 适用宿主（代码事实）

- `android`
- `ios`
- `mac`

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

- android: `android/ChromecastDisplaySkill.kt`
- ios: `ios/ChromecastPluginEntry.swift`
- mac: `mac/src/mac_edge/plugins/xiaomi_tv_display.py`

## 相关配置

- `MAC_EDGE_DISPLAY_BACKEND`
- `MAC_EDGE_XIAOMI_TV`
- `MAC_EDGE_XIAOMI_TV_HOST`
- `MAC_EDGE_XIAOMI_TV_NAME`


- 定义层来源：`ads`、`package:chromecast-display`、`package:xiaomi-tv-display`、`service:chromecast.display`、`service:xiaomi.tv.display`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
