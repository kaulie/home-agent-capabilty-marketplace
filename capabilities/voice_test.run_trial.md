# `voice_test.run_trial`

台灯语音控制实验 · 台灯语音控制实验器

kind=`action` · composition=`atomic` · group=`experiment` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

实验用：用指定音色/语速播唤醒词和「打开台灯」，再拍一张看灯亮没亮，记一轮 SUCCESS/FAIL。日常「开灯/关灯」不要用本步

## 典型触发语

- 测一下语音控制台灯
- 测试台灯语音识别成功率
- 跑一轮台灯语音测试

## 不要派给它

- 关灯
- 投屏
- 日常开灯
- 知识问答
- 给用户看照片

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `command` | string | 否 | 命令文案，默认 打开台灯。日常开灯不要用本能力。 |
| `experiment_id` | string | 否 | 实验批次 id；缺省自动生成 |
| `pitch` | string | 否 | 仅 edge-tts，如 +0Hz；say 后端忽略 |
| `settle_ms` | number | 否 | 命令播放后、拍照前等待毫秒，默认 1500 |
| `speed` | number | 否 | 语速倍率，1.0 为默认；范围 0.5–2.0 |
| `voice` | string | 否 | TTS 音色，如 Tingting；缺省读 VoiceProfile |
| `volume` | number | 否 | 播放音量 0.0–1.0，afplay -v |
| `wake_word` | string | 否 | 唤醒词，默认 小书小书 |
| `wake_word_pause_ms` | number | 否 | 「小书小书」与「打开台灯/关闭台灯」之间的停顿毫秒；识别率试验变量。>2000 命令窗口高风险。默认 1500。不是 settle_ms。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 人类可读试验摘要 |
| `asset_ref` | string | 否 | 验证图 AssetRef JSON。禁止 photo_url / path。 |
| `error_reason` | string | 否 | FAIL/INVALID 原因，如 lamp_not_on / lamp_already_on |
| `latency_ms` | string | 否 | 本轮墙钟耗时毫秒 |
| `result` | string | 是 | SUCCESS / FAIL / INVALID。SUCCESS 仅当摄像头验证台灯已亮。 |
| `timeline_text` | string | 否 | 逐步墙钟：第一句/第二句触发、拍照、看图、拾音确认、最终结果 |
| `verification_result` | string | 否 | on / off / unknown |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.voice_test`

## 能力包

- `plugins/voice-lamp-test/`

## 文档

- [home-agent-os/plugins/voice-lamp-test/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/voice-lamp-test/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/voice_test/trial.py`

## 相关配置

- `MAC_EDGE_VOICE_TEST_DIR`
- `MAC_EDGE_VOICE_TEST_PROFILE`
- `MAC_EDGE_WEBCAM_DEVICE`


- 定义层来源：`ads`、`package:voice-lamp-test`、`service:local.voice_test`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
