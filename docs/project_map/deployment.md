# 部署细节

## 谁负责部署

部署**只**由部署平台完成：本机 `:4220`。

- **禁止**在 agent 进程里同步跑 deploy / restart。
- **禁止**手改 `/Users/gaolei/runtime/**`。

```bash
curl -sS -X POST http://127.0.0.1:4220/api/deploy-notify \
  -H 'content-type: application/json' \
  -d '{"serviceId":"<平台已登记的本仓 serviceId>","ref":"main"}'
```

`build.sh` 日志里的 `home-asset-capability-marketplace` **不是**契约 serviceId。以控制面登记为准。

改了声明后，线上 Brain / Gateway 要能读到新 `GET /api/v1/export` 才算规划器生效。云 Brain 若打不到本机 `:4250`，不要假定它已吃到最新广告。

## 端口与探活

唯一契约口：**`4250`**。`scripts/stop.sh` / `start.sh` **刻意不读**继承来的 `SERVICE_PORT`。

探活：`GET http://127.0.0.1:4250/health`。

**本机开发不要占用 4250**，除非确认线上实例已停。

## 运行目录

```
<runtime>/
  scripts/{start,stop,restart,sync}.sh
  server/  web/  plugins/  declarations/  catalog/ …
  backend/.env
  backend/runtime.pid
  backend/server.log
```

库在 `~/database/home-agent-capability-marketplace/`，不在 runtime。
