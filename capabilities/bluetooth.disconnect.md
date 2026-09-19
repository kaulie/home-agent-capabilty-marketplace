# `bluetooth.disconnect`

蓝牙音箱断开器

kind=`action` · composition=`atomic` · group=`-` · 声明=`是` · 在线=`否` · ⚠️ **声明未上线**（多半是可用性门控：设备/依赖/凭证没配）

## 规划器怎么认它

断开已连接的蓝牙音箱。只负责断开，不负责停歌或放歌

## 典型触发语

- 断开蓝牙
- 断开音箱
- 断开马歇尔

## 不要派给它

- TTS
- 开灯
- 放歌本身
- 连上音箱

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
