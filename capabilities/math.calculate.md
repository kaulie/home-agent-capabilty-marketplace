# `math.calculate`

Local Math · 确定性算术求值器

kind=`action` · composition=`atomic` · group=`math` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

只算能直接求值的算式（1+1、3×5、根号4），产出数字结果。应用题、单位换算、百科题不要用本步

## 典型触发语

- 1+1等于几
- 3×5
- 一百除以四
- 根号4

## 不要派给它

- 单位换算
- 复杂数学
- 应用题
- 知识问答

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `expression` | string | 是 | 纯算式或算术问句。支持四则、括号、次方/平方/立方、根号。应用题、方程、单位换算、百科类问题勿填本字段。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 如「一加一等于二。」 |
| `result` | string | 是 | 数值结果字符串，如「2」 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.math`

## 能力包

- `plugins/math-calculate/`

## 文档

- [home-agent-os/plugins/math-calculate/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/math-calculate/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/math_calculate.py`


- 定义层来源：`ads`、`package:math-calculate`、`service:local.math`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
