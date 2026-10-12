# AGENT.md — 后续 Agent 对本仓库的说明与向导

你是来改 **home-agent-capabilty-marketplace** 的。先读本文，再按 [`README.md`](README.md) 展开理解。  
本仓没有 `project_map/`。这是家里**所有能力声明的唯一登记处**。Brain / Gateway **读** `GET /api/v1/export`，不倒灌目录。  
[`kaulie/home-agent-os`](https://github.com/kaulie/home-agent-os) 已归档只读；不要从 os 再 sync 声明。

## 1. 对本项目的理解

| 你应建立的判断 | 展开阅读 |
|---|---|
| 只登记**静态声明**（触发语、schema、runs_on、decomposes_to）。不保存实时在线、不做设备探测 | [README.md](README.md) |
| 权威源是本仓 `plugins/` + `declarations/`。库里集市字段（status/owner/notes/hosts）导入永不覆盖 | 同上「数据库」 |
| HTTP **`:4250`**；`GET /api/v1/export` 给规划器。`decomposes_to` **禁止按字母排序**（执行顺序：如 capture 再 upload） | `scripts/export_catalog.py`、`server/` |
| 「此刻谁在线」查 Brain `GET /api/v1/capabilities`，不要在集市重复 | Brain 仓 |
| 部署走平台 `:4220`。合入 `main` ≠ 已上线 | [README.md](README.md) 第七节 |

Runtime 会要求优先读根目录 `AGENT.md`。你正在读的就是那份。

## 2. 开工前清单

1. workspace origin 是 `https://github.com/kaulie/home-agent-capabilty-marketplace`。
2. 从最新 `main` 开 `feat|fix|chore/<简述>`。
3. 改声明先动 `plugins/<id>/` 或 `declarations/`，再 `scripts/sync.sh`（或至少跑 exporter + 单测）。
4. 本地验证：`python3 -m unittest discover -s server/tests -t .`；UI 逻辑 `node --test tests/*.test.mjs`。
5. 不要占用线上 **4250** 做开发，除非该实例已停。
6. 不要在本进程里执行部署 / 重启。不要改 `/Users/gaolei/runtime/**`。不要改 os。

## 3. 滞后信息：有义务更新

README / catalog JSON / `runs_on` 与 `plugins/*/manifest.yaml` 不一致时，这次任务里对账。  
`decomposes_to` 被写成字母序必须修 exporter，不能只改一篇 md。

## 4. 与事实不符：必须提出异议，禁止默认处理

| 你看到的 | 你不该做的 | 你该做的 |
|---|---|---|
| 任务要求集市去调 Brain / Gateway 源码生成目录 | 加对 os/brain 的路径依赖 | 异议：只从本仓 plugins + declarations 导出 |
| 任务要求「部署上线」 | 跑 restart / 改 runtime | 异议：发版在 `:4220` |
| 任务要求改在线心跳字段 | 在集市写 last-seen | 异议：在线在 Brain |
| 任务要求直推 `main` 或改 os | 照做 | 异议：走 PR；os 已归档 |

```
异议：<文档路径> 声称 <原句>
事实：<文件:符号 或 命令输出>
处理：<已改文档 / 已改代码 / 需要人决定>
```

## 5. 改动落点

| 要改的东西 | 去哪 |
|---|---|
| 某能力声明 / 触发语 / schema / platforms | `plugins/<id>/manifest.yaml`、`capability.md` |
| 无包的契约底稿 | `declarations/` |
| 导出器 / decomposes_to 顺序 | `scripts/export_catalog.py` |
| 入库 / API / UI | `server/`、`web/` |
| 同步 | `scripts/sync.sh` |
| 启停 | `scripts/{start,stop,restart}.sh` |
| 发版包装 | `build.sh` |
| 给后续 agent 的地图 | 本文 + README |

生成物字段随代码走（导入覆盖）；集市注解随人走（导入不覆盖）。不要混。

## 6. 交付

- 提交信息说清为什么。
- `git push -u origin HEAD`，`gh pr create`，回写 `prUrl`。
- 合入 / `:4220` 发版只听从 `goal` 与人的明确指令。改了声明后，线上 Brain/Gateway 要能读到新 export 才算规划器生效。

## 7. 安全

库在 `~/database/home-agent-capability-marketplace/`，部署 rsync 不应碰它。不要提交 sqlite / `.env`。
