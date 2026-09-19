# `xiaodu.play`

小度音箱 · 小度音箱音频播放器

kind=`output` · composition=`atomic` · group=`notify` · 声明=`否` · 在线=`是` · ⚠️ **线上未声明**（来自别的 provider，不在 mac ADS 里） · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

把本步已有的 audio Asset（如论文听读产出的音频、录音）交给客厅小度音箱放出来。入参 asset_ref（必填，type=audio，常为 $asset_ref）。用户没说是哪份音频时，先排 asset.inventory（type=audio, order=newest_first, index=1）再接本步。本步只放声音，不念文案（那是 xiaodu.speak）、不投屏、不放歌

## 典型触发语

- 把最新的音频用小度音箱播放
- 让小度音箱放这段音频
- 小度播放最新的录音
- 用客厅音箱放这段音频

## 不要派给它

- 念一段文案
- 投屏
- 点歌放歌
- Mac 本机播报
- TTS 生成

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type: "audio", mime_type?}。禁止 path / 永久 URL。常为 $asset_ref。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_id` | string | 否 | 实际播放的 audio asset_id |
| `status_text` | string | 是 | 中文一句话，如「已在小度音箱播放最新音频」 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `xiaodu.speaker` |

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
