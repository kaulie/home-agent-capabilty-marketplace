# `game.input`

TV Game Input · 游戏语音/手势输入

kind=`input` · composition=`atomic` · group=`game` · 声明=`是` · 执行前自检=`无`

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

## 适用宿主（代码事实）

- `ios`

## 服务声明

- `iphone.game.input`

## 能力包

- `plugins/tv-game-input/`

## 文档

- [plugins/tv-game-input/capability.md](../plugins/tv-game-input/capability.md)

## 入口

- ios: `ios/GameInputPluginEntry.swift`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `c272647`），请勿手改。</sub>
