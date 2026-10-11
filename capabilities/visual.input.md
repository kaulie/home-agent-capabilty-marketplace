# `visual.input`

纸质文档扫描器

kind=`input` · composition=`atomic` · group=`document` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

纸质扫描的兼容入口：同样用手机文档扫描把小票/文件收成 Image Asset。不读字、不算账

## 典型触发语

- 扫一下小票
- 扫一下这个
- 扫描一下

## 不要派给它

- OCR
- 投屏
- 看图理解
- 金额识别

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `mode` | string | 否 | 默认 document |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | Image AssetRef JSON。禁止 photo_url / path / 永久 URL。 |
| `status` | string | 是 | completed 或 cancelled |

## 服务声明

- `document.scanner`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `c272647`），请勿手改。</sub>
