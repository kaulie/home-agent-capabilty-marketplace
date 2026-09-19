# `lock.status`

小米门锁 · 门锁状态读取器

kind=`input` · composition=`atomic` · group=`lock` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

只读门锁现在锁没锁、门开没开。不能远程开锁、不能开门。用户说「门锁开了吗」用本步

## 典型触发语

- 门关了吗
- 门有没有锁上
- 门锁开了吗
- 门锁状态

## 不要派给它

- 开灯
- 开门
- 知识问答
- 远程开锁

## 入参

（无）

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `door` | string | 否 | closed / open / ajar / unknown |
| `locked` | string | 否 | locked / unlocked |
| `online` | boolean | 是 | 门锁云端是否在线 |
| `status_text` | string | 是 | 人类可读状态，如「已上锁，门关着」 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `entry.lock`

## 能力包

- `plugins/xiaomi-lock/`

## 文档

- [home-agent-os/plugins/xiaomi-lock/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/xiaomi-lock/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/xiaomi_lock.py`

## 相关配置

- `MAC_EDGE_XIAOMI_LOCK_DID`
- `MAC_EDGE_XIAOMI_PASSWORD`
- `MAC_EDGE_XIAOMI_USERNAME`


- 定义层来源：`ads`、`package:xiaomi-lock`、`service:entry.lock`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
