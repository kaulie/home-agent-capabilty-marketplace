# `pronunciation.assess`

Pronunciation Assessment · 整段英文朗读评测器

kind=`action` · composition=`atomic` · group=`pronunciation` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

给定标准朗读音频和小朋友跟读音频（均为音频 AssetRef），做整段→整段英文朗读评测，给出总分、发音准确度、流利度、完整度、韵律、重点问题单词/音素及时间位置。入参 reference_audio + student_audio。自己不录音、不上传音频、不 TTS、不投屏。两段音频须由上游上传步产出 Asset 并经 context 接进本步

## 典型触发语

- assess my reading
- pronunciation check
- 给这次朗读打分
- 评估发音
- 评测这段跟读
- 这次读得怎么样

## 不要派给它

- TTS
- 上传音频
- 单句打分
- 录音本身
- 投屏
- 拍照
- 知识问答

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `reference_audio` | string | 是 | AssetRef JSON {asset_id, type:audio, mime_type?}。标准英文朗读音频。禁止 path / 永久 URL / base64。常为 $reference_audio。 |
| `student_audio` | string | 是 | AssetRef JSON {asset_id, type:audio, mime_type?}。小朋友跟读的整段英文音频。禁止 path / 永久 URL / base64。常为 $student_audio。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `accuracy_score` | number | 是 | 发音准确度 0..100 |
| `completeness_score` | number | 是 | 完整度 0..100 |
| `duration` | object | 是 | {reference, student} 两段音频时长（秒） |
| `feedback_text` | string | 是 | 给人看的中文一句话总结，供 Brain 组装 presentation |
| `fluency` | object | 是 | {speech_rate, pause_count, long_pause_count, repetition_count} |
| `fluency_score` | number | 是 | 流利度 0..100 |
| `overall_score` | number | 是 | 整段朗读总体评分 0..100 |
| `problem_phonemes` | array | 是 | 重点问题音素 [{phoneme, word, start, end}] |
| `problem_words` | array | 是 | 重点问题单词 [{word, score, start, end, phoneme_errors, reason?}] |
| `prosody_score` | number | 是 | 韵律/重音表现 0..100 |
| `raw_alignment` | array | 是 | 逐词对齐明细，供调试/UI 展开 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.pronunciation`

## 能力包

- `plugins/pronunciation-assess/`

## 文档

- [home-agent-os/plugins/pronunciation-assess/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/pronunciation-assess/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/pronunciation_assess.py`

## 相关配置

- `MAC_EDGE_PRONUNCIATION_HEALTH_URL`
- `MAC_EDGE_PRONUNCIATION_URL`


- 定义层来源：`ads`、`package:pronunciation-assess`、`service:local.pronunciation`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
