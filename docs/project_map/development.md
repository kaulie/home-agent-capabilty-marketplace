# 开发流程

## 工作区

origin 只能是 `https://github.com/kaulie/home-agent-capabilty-marketplace`。不要改 `/Users/gaolei/runtime/**`，不要改归档 os。

## 分支

从最新 `origin/main` 开短命分支，PR 回 `main`。禁止直推 / force push `main`。已有 `prUrl` 不再开第二个 PR。

## 改代码时的边界

1. 先读 [`../../AGENT.md`](../../AGENT.md) 与本目录。
2. 改某能力声明：先动 `plugins/<id>/manifest.yaml`（及 `capability.md`），或 `declarations/`。
3. 再 `scripts/sync.sh`（或至少跑 exporter + 单测）。
4. `decomposes_to` 被写成字母序：修 `scripts/export_catalog.py`，不要只改文档。
5. 不要让集市去 import Brain / Gateway 源码生成目录。
6. 不要在本仓写 last-seen / 在线心跳。

## 测试

```bash
python3 -m unittest discover -s server/tests -t .
node --test tests/*.test.mjs
python3 tests/catalog-schema.test.py
```

## 提交与敏感物

不要提交 sqlite / `.env`。catalog JSON 回写可以进 git（对账用），库文件不行。
