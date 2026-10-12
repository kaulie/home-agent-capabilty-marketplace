# 发布细节

一次发布 = 部署平台对某个 git ref 跑仓库根 `build.sh`，得到 `outputs/`，再 rsync 到 runtime。

本仓库没有「本地一键上线」脚本。合入 `main` ≠ 已上线。

## `build.sh` 约定

- cwd = 仓库根；`APP_VERSION` = 8 位短 hash。
- 必须产出 `outputs/`，且含 `scripts/restart.sh`。
- 先 `compileall` + `unittest`（`server/tests`、`tests/catalog-schema.test.py`、`tests.test_export_catalog`），失败即不打包。
- 拷贝：`server/`、`web/`、`catalog/`、`capabilities/`、`schema/`、`tests/`、`plugins/`、`declarations/`、`bin/marketplace`、启停与 sync 脚本。
- 纯标准库：不把 venv 打进包。
- 不进包：sqlite 库、`.env`、`__pycache__`。
