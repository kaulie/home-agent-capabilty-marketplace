# `display.pdf.zoom`

PDF 投屏缩放器

kind=`output` · composition=`atomic` · group=`-` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

电视正在投屏 PDF 时放大/缩小当前页画面：中心区域按档位无损重渲染再投（1.0→1.5→2→3→4 倍）。入参 action=in（默认）/out/reset。不需要 asset_ref——缩放的是当前投屏会话里那份 PDF。翻页后自动回到原图

## 典型触发语

- 放大一点
- 电视放大
- 电视缩小
- 电视还原
- 看不清，放大

## 不要派给它

- 打印
- 打开 PDF
- 投屏新文档
- 照片放大
- 翻页

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `action` | string | 否 | in（默认）/ out / reset；也接受 放大/缩小/还原 等中文 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `page` | number | 是 | 当前投屏页码（1-based） |
| `page_count` | number | 是 | PDF 总页数 |
| `status_text` | string | 是 | 中文一句话，如「已放大到 2 倍（第 2 页 / 共 12 页）」 |
| `zoom` | number | 是 | 缩放后倍数（1.0 = 原图） |

## 服务声明

- `chromecast.display`
- `xiaomi.tv.display`

## 条件声明

- `PDF_DISPLAY_CAPABILITIES`（按依赖/后端决定是否挂上）


- 定义层来源：`ads`、`caps:PDF_DISPLAY_CAPABILITIES`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
