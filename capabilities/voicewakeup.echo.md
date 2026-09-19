# `voicewakeup.echo`

唤醒回声

kind=`output` · composition=`atomic` · group=`-` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

用户喊唤醒词之后，语音入口本机立刻回一句（如「又咋了」）。不是提醒、不是念答案、不是报时，不要排进用户任务计划

## 典型触发语

- 系统内部唤醒回声（非用户指令）

## 不要派给它

- 作为计划逐步执行
- 念答案
- 报时
- 控制设备
- 提醒
- 普通播报
- 知识问答

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `text` | string | 否 | 回声文案；缺省为又咋了 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `echo_text` | string | 是 | 实际念出的文案 |

## 服务声明

- `local.voice`


- 定义层来源：`ads`、`service:local.voice`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
