# `xiaodu.play`

小度音箱播放 · 小度音箱音频播放器

kind=`output` · composition=`atomic` · group=`notify` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把一条可拉流的 http(s) 音频 URL 交给客厅小度 DLNA 播放（SetAVTransportURI+Play）。入参 url（直接播）或 song（先解析出音频 URL 再播）或 asset_ref（已有 audio Asset，常为 $asset_ref）。用户说「用小度音箱播放歌曲十年」用本步，不要改派 music.play（那是本机网易云开播）。不念文案（xiaodu.speak）、不投屏

## 典型触发语

- 把最新的音频用小度音箱播放
- 用小度播放
- 用小度音箱播放歌曲十年
- 让小度音箱放这段音频

## 不要派给它

- Mac 本机播报
- TTS 生成
- 念一段文案
- 投屏
- 本机网易云开播

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artist` | string | 否 | 歌手，仅收窄搜索 |
| `asset_ref` | string | 否 | AssetRef JSON {asset_id, type: "audio", mime_type?}。常为 $asset_ref。 |
| `song` | string | 否 | 歌名；无 url 时先解析出音频 URL 再交给小度 |
| `url` | string | 否 | 可拉流的 http(s) 音频地址；有则直接交给小度 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_id` | string | 否 | 实际播放的 audio asset_id |
| `status_text` | string | 是 | 中文一句话，如「已在小度音箱播放最新音频」 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `xiaodu.play`

## 能力包

- `plugins/xiaodu-play/`

## 文档

- [plugins/xiaodu-play/capability.md](../plugins/xiaodu-play/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/xiaodu_speaker.py`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `c272647`），请勿手改。</sub>
