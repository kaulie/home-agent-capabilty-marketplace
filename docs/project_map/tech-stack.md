# 技术栈

以 `server/`、`web/`、`build.sh` 为准。不列计划中的栈。

| 项 | 事实 |
|---|---|
| 语言 | Python 3（**标准库 only** 服务端） |
| 入口 | `server/catalog_cli.py serve` |
| UI | 静态 HTML/JS（`web/`）；筛选逻辑有 `node --test` |
| 库 | SQLite |
| 单测 | `unittest`（`server/tests/`、`tests/`）+ `node --test tests/*.test.mjs` |

## 构建

| 工具 | 用途 |
|---|---|
| `build.sh` | compileall + 单测 + 拷进 `outputs/`（不装 pip 依赖） |
| `scripts/sync.sh` | 导出 → 入库 → 回写仓库 catalog |
| `scripts/export_catalog.py` | 声明导出；必须保序 `decomposes_to` |

无 Docker 作为一等部署路径。本检出无 `.github/workflows`。无根 `requirements.txt`（故意）。

## 本仓库没有的东西

- 无 Flask / FastAPI
- 无设备 SDK、无 OCR / Whisper
- 无应用内发版 API
