# `chat.smalltalk`

Local Chat · 闲聊问候回复器

kind=`action` · composition=`atomic` · group=`chat` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

只接纯寒暄：早啊、你好、谢谢、再见、在吗。疑问句、你会/你可以/能不能、要办事的口令都不要用本步

## 典型触发语

- 早啊
- 你好啊
- 谢谢
- 再见
- 在吗
- 早上好

## 不要派给它

- 知识问答
- 算式
- 报时
- 看图
- 拍照
- 投屏
- 控制设备
- 能力介绍
- 你会…吗
- 你可以…吗
- 能不能…

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `text` | string | 是 | 用户的话 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `reply` | string | 是 | 回复的话 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `local.chat` |

## 服务声明

- `local.chat`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`service:local.chat`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
