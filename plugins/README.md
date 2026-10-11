# 能力包（声明层）

这里是能力集市的**插件声明**：`manifest.yaml` + `capability.md`。

- 新能力先在这里登记，再由 brain / gateway 实现和心跳广告。
- 不要从 home-agent-os / brain / gateway 倒灌。
- 契约字段（role / 触发语 / input_schema）在 [`../declarations/capabilities.json`](../declarations/capabilities.json)；改完跑 `scripts/sync.sh`。
