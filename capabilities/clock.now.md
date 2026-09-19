# `clock.now`

Local Clock · 本机时钟读取器

kind=`input` · composition=`atomic` · group=`clock` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

读执行边本机墙上钟，回答「现在几点了」「今天几号」。一次性读取，应当排进计划。产出 now_iso 和给人听的 time_text。不要用文本问答编时刻

## 典型触发语

- 今天几号
- 今天日期
- 几号了
- 几月几号
- 几点了
- 现在几点了
- 现在时间

## 不要派给它

- 看图
- 知识问答
- 编一个时刻
- 计算

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `timezone` | string | 否 | IANA 时区，如 Asia/Shanghai；缺省为本机本地时区 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `now_iso` | string | 是 | ISO-8601 时刻，含 UTC 偏移 |
| `time_text` | string | 是 | 给人听/看的中文时刻（现在是…点…分）；时区在 now_iso，不要念 IANA 名或 UTC+08:00 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.clock`

## 能力包

- `plugins/clock-now/`

## 文档

- [home-agent-os/plugins/clock-now/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/clock-now/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/clock_now.py`


- 定义层来源：`ads`、`package:clock-now`、`service:local.clock`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
