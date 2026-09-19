# `game.input`

TV Game Input · 游戏语音/手势输入

kind=`input` · composition=`atomic` · group=`game` · 声明=`是` · 在线=`否` · ⚠️ **声明未上线**（多半是可用性门控：设备/依赖/凭证没配）

## 规划器怎么认它

iPhone 游戏遥控器：本地 ASR + 人体姿态识别，转 GameCommand 直送电视。常驻输入，不是 plan 逐步执行

## 典型触发语

- 挥手玩游戏
- 游戏遥控器

## 不要派给它

- 作为计划逐步执行
- 投屏单图
- 知识问答

## 入参

（无）

## 出参

（无）

## 谁提供

（当前没有在线节点广告它）

## 能力包

- `plugins/tv-game-input/`

## 文档

- [home-agent-os/plugins/tv-game-input/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/tv-game-input/capability.md)

## 可用性

- 执行前探测（checker）：无
- 当前在线：否

- 定义层来源：`ads`、`package:tv-game-input`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
