# Service: xiaodu.play

小度音箱 **音频 URL 播放** 插件（`xiaodu-play`），group=`notify`。

与 `xiaodu.speaker`（`xiaodu.speak` TTS 播报）**是两个独立插件**：本能力不合成语音，只把一条可拉流的 `http(s)` 地址交给小度 DLNA（SetAVTransportURI + Play）。

**Brain 不执行、不持有设备密钥**；只通过心跳看到 `xiaodu.play`，再把 plan 派到「现场探测到小度」的 Mac Edge。

## 规划自描述

| 字段 | 值 |
|------|-----|
| role | 小度音箱音频播放器 |
| planner_recognize | 把一条可拉流的 http(s) 音频 URL 交给客厅小度 DLNA 播放 |
| typical_triggers | `用小度音箱播放歌曲十年`、`用小度播放`、`把最新的音频用小度音箱播放` |
| do_not_dispatch | 本机网易云开播、念一段文案、投屏、Mac 本机播报、TTS 生成 |

## 标识

| 字段 | 值 |
|------|-----|
| plugin id | `xiaodu-play` |
| service_id | `xiaodu.play` |
| group | `notify` |
| wire capability | `xiaodu.play` |
| 执行方 | Mac Edge（与 `xiaodu-speaker` 共用 DLNA 探测，但是独立服务） |

## 契约

| 方向 | 内容 |
|------|------|
| **输入** | `url`（可选，可拉流的 http(s) 音频）；`song`（可选，无 url 时先解析出音频 URL）；`artist`（可选）；`asset_ref`（可选，已有 audio Asset） |
| **输出** | `status_text`（必填）；`asset_id` / `song`（可选） |

三者至少提供一种：`url` / `song` / `asset_ref`。  
**不**开本机网易云、**不**走 BlackHole 假开播、**不**念文案。

## 示例 plan

用户：「用小度音箱播放歌曲十年」

```json
{
  "execution_plan": [
    {
      "step": 1,
      "capability": "xiaodu.play",
      "input_constrict": {
        "song": "十年",
        "user_input": "用小度音箱播放歌曲十年"
      }
    }
  ]
}
```
