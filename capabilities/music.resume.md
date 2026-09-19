# `music.resume`

网易云音乐 · 继续播放器

kind=`action` · composition=`atomic` · group=`music` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

从暂停处继续刚才那首，不换歌。用户说「继续放」用本步

## 典型触发语

- 恢复播放
- 接着放
- 继续播放

## 不要派给它

- TTS
- 下一首
- 暂停
- 蓝牙连接
- 选歌

## 入参

（无）

## 出参

（无）

## 适用宿主（代码事实）

- `android`
- `ios`
- `mac`

## 服务声明

- `netease.music`

## 能力包

- `plugins/netease-music/`

## 文档

- [home-agent-os/plugins/netease-music/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/netease-music/capability.md)

## 入口

- android: `android/NetEaseMusicSkill.kt`
- ios: `ios/NetEasePluginEntry.swift`
- mac: `mac/src/mac_edge/plugins/netease_music.py`


- 定义层来源：`ads`、`package:netease-music`、`service:netease.music`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
