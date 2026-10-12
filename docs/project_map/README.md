# project_map — home-agent-capabilty-marketplace 项目地图

本目录按**运行事实**说明本仓库，不是概念词典。

GitHub 仓名是 **`home-agent-capabilty-marketplace`**（capability 少一个 i）。这是历史拼写，链接与 origin 都用这个名字，不要「纠正」成 capability。

| 文档 | 维度 |
|---|---|
| [positioning.md](positioning.md) | 项目定位：声明权威、不解决什么 |
| [architecture.md](architecture.md) | 服务架构：plugins、导出器、库、HTTP、UI |
| [tech-stack.md](tech-stack.md) | 技术栈 |
| [deployment.md](deployment.md) | 部署：谁部署、端口、库落点 |
| [release.md](release.md) | 发布：`build.sh`、单测门槛 |
| [development.md](development.md) | 开发：改声明、sync、测试 |

根目录 [`AGENT.md`](../../AGENT.md) 是后续 agent 的入口。协议细节仍在 [`README.md`](../../README.md)。

## 怎么读

1. 先读 [positioning.md](positioning.md) 和 [architecture.md](architecture.md)。
2. 动手前对照：权威源 `plugins/` + `declarations/`；导出 `scripts/export_catalog.py`；入库 `server/`。
3. 发现本目录或 README 与代码不一致时，按 [`AGENT.md`](../../AGENT.md) 处理。

## 本轮已核对的异议（2026-10-12）

1. **Brain / Gateway 只读 `GET /api/v1/export`。** 不要从 os / brain / gateway 倒灌目录，也不要再从归档 os sync。
2. **`decomposes_to` 禁止按字母排序。** 它是执行顺序（例如 capture 再 upload）。写错必须改 exporter，不能只改一篇 md。
3. **生成物字段随代码走，集市注解随人走。** 导入覆盖 kind/schema/runs_on；永不覆盖 status/owner/notes/hosts。
4. **「此刻谁在线」在 Brain** `GET /api/v1/capabilities`，不在集市。
5. **`build.sh` 的 echo 写成了 `home-asset-capability-marketplace`。** 这不是 GitHub 仓名，也不是可靠的平台 serviceId。发版用控制面里已经登记的那条。
6. **本检出无 `.github/workflows`。** `build.sh` 本地会跑 compileall + 单测。

后续 agent 若发现上述条目被新代码推翻，删除或改写，不要累积过期异议。
