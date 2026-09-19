# `web.scraper`

网页抓取器（URL → 核心正文/整页 → PDF/文本） · 网页抓取器（URL / url 资产 → 核心正文/整页 → PDF/文本）

kind=`action` · composition=`atomic` · group=`convert` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

用户给一个 http(s) 网址、或引用已登记的 Brain url 资产（type=url），要求把网页抓下来存成 PDF 或文本时用本步。入参 url（必填其一，http/https）与 asset_ref（可选，type=url 的 Brain url 资产，二选一）；mode=article 抓核心正文（默认，剔除广告/导航）/ page 抓忠实整页；format=pdf（默认）/ text；renderer=auto/weasyprint/chrome（仅 pdf，本机自动挑可用引擎）；page_numbers 默认 true（每页页脚加页码，page_number_style=cn 中文「第 N 页 / 共 M 页」/ numeric 数字「N / M」；native_header_footer=true 改用 Chrome 原生页脚）。产出登记为新 document Asset，可交给 printer.print 打印或后续流程。本步只抓网页转文档，不打印、不问答

## 典型触发语

- 保存这个网页
- 把我存的链接转成 PDF
- 把网址 http… 的文章转成 PDF
- 把网页正文导出成文本
- 把这个网页存成 PDF
- 抓取这篇文章转成 PDF
- 网页转 PDF

## 不要派给它

- OCR
- 下载图片
- 打印
- 投屏
- 整页截图
- 浏览网页问答
- 看图理解
- 翻译
- 配网

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 否 | 已登记的 Brain url 资产（type=url）AssetRef；与 url 二选一，填了就抓该链接。例 {"asset_id":"asset_…","type":"url"}。 |
| `format` | string | 否 | pdf=PDF 文档（默认）/ text=纯文本；也接受 文本。 |
| `mode` | string | 否 | article=抓核心正文（默认，剔除广告/导航）/ page=忠实整页；也接受 正文/整页 等中文。 |
| `name` | string | 否 | 可选产物展示名（自动补 .pdf/.txt）；不传则 web-scraper-<时间戳>-<mode>.*。 |
| `native_header_footer` | boolean | 否 | pdf 时生效：默认 false。true=改用 Chrome 原生页眉页脚（带日期与 URL，自带 N/M 页码），此时不再叠加页码层。 |
| `page_number_style` | string | 否 | 页脚样式：cn=「第 N 页 / 共 M 页」（默认）/ numeric=「N / M」；也接受 中文/数字。 |
| `page_numbers` | boolean | 否 | pdf 时生效：是否加页码，默认 true。false=完全不加（保持旧行为）。 |
| `renderer` | string | 否 | pdf 时生效：auto=自动（默认，Chrome 优先；weasyprint 有字形渲染问题见 #671，可显式选它做对比）/ weasyprint / chrome。 |
| `url` | string | 是 | 网页地址（http/https），与 asset_ref 二选一；给了 asset_ref(type=url) 时可省。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 抓取产物 document AssetRef（PDF application/pdf 或文本 text/plain） |
| `char_count` | number | 否 | 导出文本字符数 |
| `format` | string | 是 | pdf / text |
| `mode` | string | 是 | article / page |
| `native_header_footer` | boolean | 否 | 是否走了 Chrome 原生页脚（pdf 时） |
| `page_count` | number | 否 | PDF 页数（pdf 时） |
| `page_number_style` | string | 否 | 实际页码样式：cn / numeric（pdf 时） |
| `page_numbers` | boolean | 否 | pdf 时：页码是否真的生效（true=已叠加或用了原生页脚；false=已关闭或本机无 Chrome 降级） |
| `renderer` | string | 否 | 实际使用的渲染引擎（pdf 时）：weasyprint / chrome |
| `status_text` | string | 是 | 中文一句话结果，含页数/字数、引擎与 asset_id |
| `title` | string | 是 | 网页标题 |
| `url` | string | 是 | 抓取到的最终 URL（跟随重定向后） |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.web.scraper`

## 能力包

- `plugins/web-scraper/`

## 文档

- [home-agent-os/plugins/web-scraper/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/web-scraper/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/web_scraper.py`


- 定义层来源：`ads`、`package:web-scraper`、`service:local.web.scraper`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
