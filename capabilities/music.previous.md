# `music.previous`

网易云音乐 · 上一首切换器

kind=`action` · composition=`atomic` · group=`music` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

切回播放队列的上一首。用户说「上一首/上一曲」用本步

## 典型触发语

- 上一曲
- 上一首

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

- [plugins/netease-music/capability.md](../plugins/netease-music/capability.md)

## 入口

- android: `android/NetEaseMusicSkill.kt`
- ios: `ios/NetEasePluginEntry.swift`
- mac: `mac/src/mac_edge/plugins/netease_music.py`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `c272647`），请勿手改。</sub>
