# `notify.speak`

语音播报器

kind=`output` · composition=`atomic` · group=`-` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

把用户指定的提醒/公告原文念出来，例如「五分钟后提醒萱萱关电视」「大声说该喝水了」。入参 text=要念的那句话。不要用来回读其它步骤的答案；那种情况用 presentation.type=audio，由控制面补播

## 典型触发语

- 一分钟后说
- 大声念出来
- 提醒我说
- 提醒萱萱
- 该喝水了

## 不要派给它

- 唤醒应答
- 念出执行结果
- 把答案用语音告诉我
- 投图
- 拍照
- 用语音播放结果
- 知识生成

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `lang` | string | 否 | 语言提示，如 zh_CN / en_US |
| `text` | string | 是 | 要念出的文案 |
| `voice` | string | 否 | 可选 say 音色名；edge 后端时为 edge-tts 音色 |

## 出参

（无）

## 服务声明

- `local.notify`


- 定义层来源：`ads`、`service:local.notify`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
