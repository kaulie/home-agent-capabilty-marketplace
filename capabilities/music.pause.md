# `music.pause`

网易云音乐 · 暂停播放器

kind=`action` · composition=`atomic` · group=`music` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

暂停当前正在放的歌，不换歌、不选新歌。用户说「暂停一下」用本步，不是停止、不是下一首

## 典型触发语

- 先停一下
- 暂停
- 暂停播放

## 不要派给它

- TTS
- 下一首
- 停止播放
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

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
