# `document.scan`

Document Scanner · 纸质文档扫描器

kind=`input` · composition=`atomic` · group=`document` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

用手机系统文档扫描拍纸质（小票、文件、作业），直接上传成 Image Asset。只负责扫进系统，不读字、不算金额、不总结、不投屏。读字要另排 OCR

## 典型触发语

- 扫一下
- 扫一下作业
- 扫一下文档
- 扫描一下
- 扫描一下这个小票

## 不要派给它

- OCR
- 开灯
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

## 适用宿主（代码事实）

- `ios`

## 服务声明

- `document.scanner`

## 能力包

- `plugins/document-scanner/`

## 文档

- [plugins/document-scanner/capability.md](../plugins/document-scanner/capability.md)

## 入口

- ios: `ios/LivingRoomEdge/LivingRoomEdge/VisualInput/VisualInput.swift`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `c272647`），请勿手改。</sub>
