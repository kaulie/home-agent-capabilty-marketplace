# `xiaodu.control`

小度音箱 · 小度音箱播放控制器

kind=`output` · composition=`atomic` · group=`notify` · 声明=`否` · 在线=`是` · ⚠️ **线上未声明**（来自别的 provider，不在 mac ADS 里） · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

暂停 / 继续 / 停止**小度音箱当前正在播放的内容**（DLNA AVTransport）。入参 action=pause（默认）/ resume / stop，也接受 暂停/继续/停止 等中文。只控制「正在放的那段」，不放新内容（那是 xiaodu.play）、不念文案（xiaodu.speak）

## 典型触发语

- 暂停小度
- 停止小度播放
- 小度先停一下
- 继续小度播放
- 别放了

## 不要派给它

- 放新闻频
- 点歌放歌
- 念一段文案
- 投屏
- Mac 本机播报

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `action` | string | 否 | pause（默认）/ resume / stop；也接受 暂停/继续/停止 等中文 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `status_text` | string | 是 | 中文一句话，如「小度音箱已暂停」 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `xiaodu.speaker` |

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
