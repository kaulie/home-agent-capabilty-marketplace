# `display.audio.control`

小米电视 DLNA · 电视音频播放控制器

kind=`output` · composition=`atomic` · group=`display` · 声明=`否` · 在线=`是` · ⚠️ **线上未声明**（来自别的 provider，不在 mac ADS 里） · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

暂停 / 继续 / 停止**小米电视当前正在播的音频**（display.audio 播出去的那段）。入参 action=pause（默认）/ resume / stop，也接受 暂停/继续/停止 等中文。不放新内容、不投屏、不投 PDF

## 典型触发语

- 暂停电视播放
- 把电视上的音频停掉
- 电视继续播放
- 电视上的声音停一下

## 不要派给它

- 打开 PDF
- 投屏新文档
- 打印
- 单图投屏
- 放大缩小

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `action` | string | 否 | pause（默认）/ resume / stop；也接受 暂停/继续/停止 等中文 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `status_text` | string | 是 | 中文一句话，如「小米电视已暂停」 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `xiaomi.tv.display` |

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
