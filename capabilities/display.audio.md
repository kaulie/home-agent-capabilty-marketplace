# `display.audio`

小米电视 DLNA · 音频投电视播放器

kind=`output` · composition=`atomic` · group=`display` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把本步已有的 audio Asset（如论文听读产出的音频）交给电视用 DLNA 放出来。入参 asset_ref（必填，type=audio，常为 $asset_ref）。用户没说是哪份音频时，先排 asset.inventory（type=audio, order=newest_first, index=1）再接本步。本步只出声，不投图、不放歌、不做 TTS、不打印

## 典型触发语

- 在电视上放这段音频
- 把最新的音频在小米电视上放出来
- 把这段录音投到电视上放
- 让小米电视播放最新的音频

## 不要派给它

- ChromeCast 投屏
- TTS 念文本
- 打印
- 投 PDF
- 投图
- 点歌放歌

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type: "audio", mime_type?}。禁止 path / 永久 URL。常为 $asset_ref。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_id` | string | 否 | 实际播放的 audio asset_id |
| `status_text` | string | 是 | 中文一句话，如「已在小米电视播放最新音频」 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `xiaomi.tv.display`

## 条件声明

- `AUDIO_DISPLAY_CAPABILITIES`（按依赖/后端决定是否挂上）

## 能力包

- `plugins/xiaomi-tv-display/`

## 文档

- [home-agent-os/plugins/xiaomi-tv-display/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/xiaomi-tv-display/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/xiaomi_tv_display.py`

## 相关配置

- `MAC_EDGE_DISPLAY_BACKEND`
- `MAC_EDGE_XIAOMI_TV`
- `MAC_EDGE_XIAOMI_TV_HOST`
- `MAC_EDGE_XIAOMI_TV_NAME`


- 定义层来源：`ads`、`caps:AUDIO_DISPLAY_CAPABILITIES`、`package:xiaomi-tv-display`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
