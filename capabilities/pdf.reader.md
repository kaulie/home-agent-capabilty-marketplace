# `pdf.reader`

PDF 语音朗读器 · PDF 语音朗读器

kind=`action` · composition=`atomic` · group=`convert` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把本步已有的 PDF/document Asset 的文字念成一段语音（TTS 音频 Asset）：用户说「念一下这份 PDF / 把这份文档读给我听 / 朗读这个 PDF」时用本步。入参 asset_ref（必填，type=document，常为 $asset_ref），可选 page_start/page_end、speed、voice、max_chars。产出 audio AssetRef——语音入口把 presentation 设为 {type:audio, from:asset_ref} 播放这段朗读；用户没指定哪份 PDF 时，先排 asset.inventory 取最新 document 再接本步。只念文档正文，不是短提醒/公告（那种用 notify.speak）；扫描件（无文字层）本步会失败，要先 pdf.to_images + image.ocr

## 典型触发语

- 念一下这份 PDF
- 把 PDF 转成语音
- 把这份文档读给我听
- 朗读这个 PDF
- 读一遍这个文档

## 不要派给它

- OCR 识别
- PDF 旋转
- PDF 转图片
- 打印
- 投屏
- 拍照
- 提醒/公告短句播报
- 放歌
- 看图理解

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 必填 AssetRef JSON，type=document（PDF）。例 {"asset_id":"asset_…","type":"document"}。禁止 path / 永久 URL；缺则本能力无效。 |
| `lang` | string | 否 | 朗读语言（zh_CN / en_US）；不传则按正文语言自动判定（英文论文用英文音色，避免中文音色念英文的口音） |
| `max_chars` | number | 否 | 本次合成的字数上限，默认 12000（约 40 分钟语音）；0=不截断。超上限按句边界截断并在 status_text 说明 |
| `name` | string | 否 | 可选音频展示名（不含扩展名）；不传则用 pdf-<asset_id 前 12 位> |
| `page_end` | number | 否 | 结束页（1-based，闭区间），缺省最后一页；越界钳到边界 |
| `page_start` | number | 否 | 起始页（1-based），缺省第 1 页；越界钳到边界 |
| `speed` | number | 否 | 语速倍率，默认 1.0（钳制 0.5–2.0） |
| `voice` | string | 否 | 可选音色：edge-tts 音色名（如 en-US-AvaMultilingualNeural / zh-CN-YunxiNeural）或 macOS say 音色名；不传则按语言取默认音色 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 新登记的 audio AssetRef（mime audio/mpeg 或 audio/mp4）；presentation {type: audio, from: asset_ref} 即播放这段朗读 |
| `chars` | number | 是 | 实际合成为语音的字数（截断后） |
| `chars_total` | number | 是 | 所选页范围抽取到的总字数（截断前） |
| `duration_sec` | number | 否 | 音频时长（秒）；探测不到时为 null |
| `engine` | string | 是 | 实际使用的合成引擎：edge（edge-tts）/ say（macOS 本机） |
| `page_count` | number | 是 | PDF 总页数 |
| `page_end` | number | 是 | 本次朗读结束页（1-based，闭区间） |
| `page_start` | number | 是 | 本次朗读起始页（1-based） |
| `status_text` | string | 是 | 中文一句话结果，含页范围、字数、时长、引擎与 asset_id |
| `text_preview` | string | 否 | 朗读文字开头摘要（约 80 字），供对话回显 |
| `truncated` | boolean | 是 | 是否因字数上限截断（true=只念了前面一部分） |
| `voice` | string | 是 | 实际使用的音色名 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.pdf.reader`

## 能力包

- `plugins/pdf-reader/`

## 文档

- [home-agent-os/plugins/pdf-reader/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/pdf-reader/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/pdf_reader.py`

## 相关配置

- `MAC_EDGE_PDF_READER_MAX_CHARS`
- `MAC_EDGE_PDF_READER_TIMEOUT_SEC`
- `MAC_EDGE_PDF_READER_TTS_BACKEND`
- `MAC_EDGE_PDF_READER_TTS_FALLBACK_SAY`
- `MAC_EDGE_PDF_READER_VOICE`


- 定义层来源：`ads`、`package:pdf-reader`、`service:local.pdf.reader`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
