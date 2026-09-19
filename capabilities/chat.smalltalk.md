# `chat.smalltalk`

闲聊问候回复器

kind=`action` · composition=`atomic` · group=`chat` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

只接纯寒暄：早啊、你好、谢谢、再见、在吗。疑问句、你会/你可以/能不能、要办事的口令都不要用本步

## 典型触发语

- 你好啊
- 再见
- 在吗
- 早上好
- 早啊
- 谢谢

## 不要派给它

- 你会…吗
- 你可以…吗
- 投屏
- 报时
- 拍照
- 控制设备
- 看图
- 知识问答
- 算式
- 能不能…
- 能力介绍

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `text` | string | 是 | 用户的话 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `reply` | string | 是 | 回复的话 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.chat`

## 能力包

- `plugins/chat-smalltalk/`

## 文档

- [home-agent-os/plugins/chat-smalltalk/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/chat-smalltalk/capability.md)


- 定义层来源：`ads`、`package:chat-smalltalk`、`service:local.chat`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
