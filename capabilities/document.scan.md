# `document.scan`

Document Scanner · 纸质文档扫描器

kind=`input` · composition=`atomic` · group=`document` · 声明=`是` · 在线=`否` · ⚠️ **声明未上线**（多半是可用性门控：设备/依赖/凭证没配）

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

## 谁提供

（当前没有在线节点广告它）

## 能力包

- `plugins/document-scanner/`

## 文档

- [home-agent-os/plugins/document-scanner/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/document-scanner/capability.md)

## 可用性

- 执行前探测（checker）：无
- 当前在线：否

- 定义层来源：`ads`、`package:document-scanner`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
