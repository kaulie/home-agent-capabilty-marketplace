# `bluetooth.connect`

蓝牙音箱连接器

kind=`action` · composition=`atomic` · group=`-` · 声明=`是` · 在线=`否` · ⚠️ **声明未上线**（多半是可用性门控：设备/依赖/凭证没配）

## 规划器怎么认它

把 Marshall 一类蓝牙音箱连上。只负责连接，不负责选歌播放

## 典型触发语

- 连上音箱
- 连上马歇尔
- 连接音箱

## 不要派给它

- TTS
- 开灯
- 放歌本身
- 断开音箱

## 入参

（无）

## 出参

（无）

## 谁提供

（当前没有在线节点广告它）

## 可用性

- 执行前探测（checker）：无
- 当前在线：否

- 定义层来源：`ads`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
