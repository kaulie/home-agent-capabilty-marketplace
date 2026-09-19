# `music.play`

网易云音乐 · 音乐播放器

kind=`action` · composition=`atomic` · group=`music` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

从用户话里拆出歌名 song、可选作者 artist；不要把整句当 keyword。本轮必须有 song，不能只按歌手或专辑点播。不负责暂停/切歌。

## 典型触发语

- 放十年
- 播放陈奕迅的十年

## 不要派给它

- 蓝牙连接
- TTS
- 开灯
- 暂停
- 下一首
- 下载
- 缓存

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `album` | string | 否 | 专辑（本轮忽略） |
| `artist` | string | 否 | 作者，仅收窄搜索 |
| `song` | string | 否 | 歌名（本机 Mac 本轮必填） |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artist` | string | 否 | 歌手 |
| `original_id` | number | 否 | 网易云 original_id |
| `song` | string | 否 | 正在播放的歌名 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `netease.music` |

## 服务声明

- `netease.music`

## 能力包

- `plugins/netease-music/`

## 文档

- [home-agent-os/plugins/netease-music/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/netease-music/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/netease_music.py`

## 可用性

- 执行前探测（checker）：有
- 当前在线：是

- 定义层来源：`ads`、`package:netease-music`、`service:netease.music`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
