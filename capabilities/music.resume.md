# `music.resume`

网易云音乐 · 继续播放器

kind=`action` · composition=`atomic` · group=`music` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

从暂停处继续刚才那首，不换歌。用户说「继续放」用本步

## 典型触发语

- 继续播放
- 恢复播放
- 接着放

## 不要派给它

- 选歌
- 蓝牙连接
- TTS
- 暂停
- 下一首

## 入参

（无）

## 出参

（无）

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
