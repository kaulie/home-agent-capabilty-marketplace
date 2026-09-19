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

（无）

## 出参

（无）

## 适用宿主（代码事实）

- `ios`

## 能力包

- `plugins/document-scanner/`

## 文档

- [home-agent-os/plugins/document-scanner/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/document-scanner/capability.md)

## 入口

- ios: `ios/LivingRoomEdge/LivingRoomEdge/VisualInput/VisualInput.swift`


- 定义层来源：`ads`、`package:document-scanner`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
