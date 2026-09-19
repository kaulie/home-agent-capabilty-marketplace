# `capabilities.summary`

在线能力口语汇总器

kind=`system` · composition=`atomic` · group=`meta` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

用口语告诉用户此刻家里能帮什么忙，或回答「你会开灯吗」「能不能控制空调」这类会不会。只介绍，不真的去开灯/开空调，答语里不要念技术编号

## 典型触发语

- 你可以做什么
- 你能干什么
- 你会什么
- 有哪些能力
- 你可以控制空调吗
- 你会开灯吗
- 能不能控制空调

## 不要派给它

- 知识问答
- 执行开灯或开空调
- 拍照
- 逐条朗读自描述
- 在答语里念出其它能力的编号或技术名

## 入参

（无）

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 给用户听的简短口语能力介绍（非技术自描述清单） |
| `capability_count` | string | 否 | 当前在线可调度 Runtime capability 数量 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| Brain | `system` | `system.capabilities` |

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
