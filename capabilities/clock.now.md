# `clock.now`

Local Clock · 本机时钟读取器

kind=`system` · composition=`atomic` · group=`clock` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

Brain 就地读本机墙上钟，回答「现在几点了」「今天几号」。一次性读取，应当排进计划，assigned_edge_id=system。产出 now_iso 和给人听的 time_text。不要用文本问答编时刻

## 典型触发语

- 现在几点了
- 几点了
- 现在时间
- 今天几号
- 今天日期
- 几月几号
- 几号了

## 不要派给它

- 知识问答
- 计算
- 看图
- 编一个时刻

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `appliance` | string | 否 | 绑定名（如 Local Clock），仅用于多实例区分，不影响读钟 |
| `timezone` | string | 否 | IANA 时区，默认 Asia/Shanghai |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `now_iso` | string | 是 | 本机当前时间 ISO 8601（带时区），如 2026-08-27T22:30:00+08:00 |
| `time_text` | string | 是 | 给人听/看的当前时间中文，如「现在是 22 点 30 分」 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| Brain | `system` | `system.clock` |

## 服务声明

- `local.clock`

## 能力包

- `plugins/clock-now/`

## 文档

- [home-agent-os/plugins/clock-now/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/clock-now/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/clock_now.py`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`package:clock-now`、`service:local.clock`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
