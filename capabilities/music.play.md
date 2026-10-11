# `music.play`

网易云音乐 · 音乐播放器

kind=`action` · composition=`atomic` · group=`music` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

从用户话里拆出歌名 song、可选作者 artist；不要把整句当 keyword。用户说「用小度音箱播放」时不要派本步，改派 xiaodu.play。本轮必须有 song，不能只按歌手或专辑点播。不负责暂停/切歌。

## 典型触发语

- 播放陈奕迅的十年
- 放十年
- 用小度音箱播放

## 不要派给它

- TTS
- 下一首
- 下载
- 开灯
- 暂停
- 缓存
- 蓝牙连接

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `album` | string | 否 | 专辑（本轮忽略） |
| `artist` | string | 否 | 作者，仅收窄搜索 |
| `song` | string | 否 | 歌名（本机 Mac 本轮必填） |
| `speaker` | string | 否 | 输出音箱；xiaodu/小度=客厅小度 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artist` | string | 否 | 歌手 |
| `original_id` | number | 否 | 网易云 original_id |
| `song` | string | 否 | 正在播放的歌名 |

## 适用宿主（代码事实）

- `android`
- `ios`
- `mac`

## 服务声明

- `netease.music`

## 能力包

- `plugins/netease-music/`

## 文档

- [plugins/netease-music/capability.md](../plugins/netease-music/capability.md)

## 入口

- android: `android/NetEaseMusicSkill.kt`
- ios: `ios/NetEasePluginEntry.swift`
- mac: `mac/src/mac_edge/plugins/netease_music.py`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `c272647`），请勿手改。</sub>
