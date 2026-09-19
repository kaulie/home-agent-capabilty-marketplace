# `voicewakeup.echo`

Local Voice Stream · 唤醒回声

kind=`output` · composition=`atomic` · group=`voice` · 声明=`是` · 在线=`是`

## 规划器怎么认它

用户喊唤醒词之后，语音入口本机立刻回一句（如「又咋了」）。不是提醒、不是念答案、不是报时，不要排进用户任务计划

## 典型触发语

- 系统内部唤醒回声（非用户指令）

## 不要派给它

- 作为计划逐步执行
- 普通播报
- 提醒
- 念答案
- 知识问答
- 控制设备
- 报时

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `text` | string | 否 | 回声文案；缺省为又咋了 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `echo_text` | string | 是 | 实际念出的文案 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `local.voice` |

## 服务声明

- `local.voice`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`service:local.voice`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
