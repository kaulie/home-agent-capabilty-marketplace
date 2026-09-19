# `game.launch`

TV Game Cast · 电视互动游戏启动器

kind=`output` · composition=`atomic` · group=`game` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

在电视上启动指定互动游戏（接金币等）。本步必填 game_id。启动后实时语音/手势控制不走 Brain，由 iPhone 本地 GameCommand 直送电视

## 典型触发语

- 启动游戏
- 打开接金币游戏
- 打开电视游戏
- 玩接金币
- 玩游戏

## 不要派给它

- 向右
- 向左
- 实时移动
- 帧级控制
- 暂停
- 继续
- 跳

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `game_id` | string | 是 | 游戏 id，如 coin_catcher |
| `game_url` | string | 否 | 可选 LAN URL；缺省由 Mac 启动 serve.py 并返回 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `game_id` | string | 是 | 已启动的游戏 id |
| `game_url` | string | 是 | LAN 游戏页 URL（Chromecast iframe 加载） |
| `status` | string | 是 | ready |

## 适用宿主（代码事实）

- `ios`

## 服务声明

- `mac.game.host`

## 能力包

- `plugins/tv-game/`

## 文档

- [home-agent-os/plugins/tv-game/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/tv-game/capability.md)

## 入口

- ios: `ios/TvGamePluginEntry.swift`


- 定义层来源：`ads`、`package:tv-game`、`service:mac.game.host`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
