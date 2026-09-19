# `paper.read`

论文听读器 · 论文听读器（论文/长文献 → 结构化听读音频）

kind=`action` · composition=`atomic` · group=`read` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把已有的论文 PDF/document Asset 转成适合**连续听读**的音频：用户说「把这篇论文念给我听 / 听读这篇 paper / 这篇论文太长了听一遍 / 帮我听读这篇研究」时用本步。与 pdf.reader 的分工：pdf.reader 只管「念一下这份 PDF」这类通用短文档；本步面向论文/长文献，会做结构（识别章节、跳过 References 与页眉页脚、不念图表说明），并回 sections[] 索引（每节字数/页范围/估算起始秒）。入参 asset_ref（必填，type=document，常为 $asset_ref）；mode 默认 original（原文听读，忠实原文、不讲解），可选 page_start/page_end、speed、voice、max_chars。产出 audio AssetRef——语音入口把 presentation 设为 {type:audio, from:asset_ref} 播放。用户没指定哪篇论文时，先排 asset.inventory 取最新 document 再接本步。mode=explain（AI 讲解）v1 保留未交付，传了会明确失败；扫描件（无文字层）会失败，要先 pdf.to_images + image.ocr

## 典型触发语

- 听读这篇 paper
- 帮我听读这篇研究
- 把这篇论文念给我听
- 朗读这篇论文
- 这篇论文太长了，听一遍

## 不要派给它

- OCR 识别
- PDF 旋转
- PDF 转图片
- 念一份普通 PDF/说明书（用 pdf.reader）
- 打印
- 投屏
- 提醒/公告短句播报
- 放歌
- 论文总结 / Markdown 报告
- 论文问答

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 必填 AssetRef JSON，type=document（PDF 论文）。例 {"asset_id":"asset_…","type":"document"}。禁止 path / 永久 URL；缺则本能力无效。 |
| `depth` | string | 否 | explain 的讲解层数：overview（默认）/ method / deep；original 模式忽略 |
| `lang` | string | 否 | 朗读语言（zh_CN / en_US）；不传则按正文语言自动判定（英文论文用英文音色，避免中文音色念英文的口音） |
| `max_chars` | number | 否 | 本次合成的字数上限，默认 12000（约 40 分钟语音）；0=不截断。超上限按句边界截断并在 status_text 说明 |
| `mode` | string | 否 | 阅读模式，默认 original（原文听读：忠实原文、跳 References、不念图表说明）；explain（AI 讲解）v1 保留未交付，传了会明确失败 |
| `name` | string | 否 | 可选音频展示名（不含扩展名）；不传则用论文标题，再退化为 paper-<asset_id 前 12 位> |
| `page_end` | number | 否 | 结束页（1-based，闭区间），缺省最后一页；越界钳到边界 |
| `page_start` | number | 否 | 起始页（1-based），缺省第 1 页；越界钳到边界 |
| `speed` | number | 否 | 语速倍率，默认 1.0（钳制 0.5–2.0） |
| `voice` | string | 否 | 可选音色：edge-tts 音色名（如 en-US-AvaMultilingualNeural / zh-CN-YunxiNeural）或 macOS say 音色名；不传则按语言取默认音色 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 新登记的 audio AssetRef（mime audio/mpeg 或 audio/mp4）；presentation {type: audio, from: asset_ref} 即播放这段听读音频 |
| `chars` | number | 是 | 实际合成为语音的字数（截断后） |
| `chars_total` | number | 是 | 清洗后完整听读稿的字数（截断前） |
| `depth` | string | 否 | explain 模式回显的讲解层数；original 为 null |
| `duration_sec` | number | 否 | 音频时长（秒）；探测不到时为 null |
| `engine` | string | 是 | 实际使用的合成引擎：edge（edge-tts）/ say（macOS 本机） |
| `mode` | string | 是 | 本次实际使用的模式（original / explain） |
| `page_count` | number | 是 | PDF 总页数 |
| `page_end` | number | 是 | 本次听读结束页（1-based，闭区间） |
| `page_start` | number | 是 | 本次听读起始页（1-based） |
| `sections` | object | 是 | section 级索引数组：每项 {index, type, heading, chars, page_start, page_end, est_offset_sec}（est_offset_sec 为估算起始秒） |
| `sections_count` | number | 是 | 识别到的章节数 |
| `status_text` | string | 是 | 中文一句话结果，含模式、页范围、章节数、字数、时长、是否截断与引擎 |
| `text_preview` | string | 否 | 听读稿开头摘要（约 80 字），供对话回显 |
| `title` | string | 否 | 识别到的论文标题；识别不到为 null |
| `truncated` | boolean | 是 | 是否因字数上限截断（true=只念了前面一部分） |
| `voice` | string | 是 | 实际使用的音色名 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.paper.read`

## 能力包

- `plugins/paper-reader/`

## 文档

- [home-agent-os/plugins/paper-reader/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/paper-reader/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/paper_read.py`

## 相关配置

- `MAC_EDGE_PAPER_READ_MAX_CHARS`
- `MAC_EDGE_PDF_READER_TIMEOUT_SEC`
- `MAC_EDGE_PDF_READER_TTS_BACKEND`
- `MAC_EDGE_PDF_READER_TTS_FALLBACK_SAY`
- `MAC_EDGE_PDF_READER_VOICE`


- 定义层来源：`ads`、`package:paper-reader`、`service:local.paper.read`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
