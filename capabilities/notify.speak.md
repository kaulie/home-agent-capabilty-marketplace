# `notify.speak`

Local Notify · 语音播报器

kind=`output` · composition=`atomic` · group=`notify` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

把用户指定的提醒/公告原文念出来，例如「五分钟后提醒萱萱关电视」「大声说该喝水了」。入参 text=要念的那句话。不要用来回读其它步骤的答案；那种情况用 presentation.type=audio，由控制面补播

## 典型触发语

- 大声念出来
- 提醒我说
- 一分钟后说
- 提醒萱萱
- 该喝水了

## 不要派给它

- 知识生成
- 拍照
- 投图
- 唤醒应答
- 把答案用语音告诉我
- 用语音播放结果
- 念出执行结果

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `lang` | string | 否 | 语言提示，如 zh_CN / en_US |
| `text` | string | 是 | 要念出的文案 |
| `voice` | string | 否 | 可选 say 音色名；edge 后端时为 edge-tts 音色 |

## 出参

（无）

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `local.notify` |

## 服务声明

- `local.notify`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`service:local.notify`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
