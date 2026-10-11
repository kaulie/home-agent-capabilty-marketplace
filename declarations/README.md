# 定义层快照

`capabilities.json` 是规划器广告 / 入参出参 / 服务归属的权威底稿。

一次性从冻结前的 home-agent-os 导出迁入，之后只在本仓改。导出器 `scripts/export_catalog.py` 把它与 `plugins/` 合并，不读其它仓库。
