# 项目定位

## 一句话

home-agent-capabilty-marketplace 是家里**所有能力声明的唯一登记处**：触发语、schema、runs_on、decomposes_to、评审注解。它不保存实时在线，不做设备探测，不执行能力。

仓库：[`https://github.com/kaulie/home-agent-capabilty-marketplace`](https://github.com/kaulie/home-agent-capabilty-marketplace)  
契约端口：`4250`

## 它要解决什么

```
plugins/<id>/manifest.yaml + capability.md     权威源（有包）
declarations/                                  契约底稿（无包）
        │
        ▼  scripts/export_catalog.py
   catalog JSON
        │
        ▼  入库（覆盖生成物，保留注解）
   SQLite + GET /api/v1/export
        │
        ▼
   Brain / Gateway 规划器广告
```

规划器吃 export，不倒灌。人在 UI 里改的是集市字段（status / owner / notes / hosts）。

## 它不是什么

| 不是 | 谁才是 |
|---|---|
| 规划器 / intent 队列 | [`home-agent-brain`](https://github.com/kaulie/home-agent-brain) |
| 设备 I/O | [`home-agent-gateway`](https://github.com/kaulie/home-agent-gateway) |
| 在线心跳表 | Brain `GET /api/v1/capabilities` |
| OCR / 指字 / 发音引擎 | 三个 sidecar 仓 |
| 已冻结的单体 os | [`home-agent-os`](https://github.com/kaulie/home-agent-os)（归档只读） |

本仓库**没有**「对本机 runtime 发起部署」的 HTTP 入口。上线走 `:4220`。

## 当前形态

- HTTP：`python3 server/catalog_cli.py serve`（默认 `:4250`）
- UI：服务版 `http://127.0.0.1:4250/`；`web/index.html` 也可静态托管
- 纯标准库服务端（不需要 pip/venv）
- 发版包装 `build.sh` + `scripts/{start,stop,restart,sync}.sh`
