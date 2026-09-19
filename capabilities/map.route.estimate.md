# `map.route.estimate`

路线距离与耗时查询器

kind=`system` · composition=`atomic` · group=`map` · 声明=`否` · 在线=`是` · ⚠️ **线上未声明**（来自别的 provider，不在 mac ADS 里） · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

查两地之间的驾车/公交地铁/步行距离与预计耗时，基于高德地图实时路网。入参 origin、destination 必填；mode 可选 driving|transit|walking（默认 driving）。assigned_edge_id=system。产出 answer_text、distance_km、duration_min。用户问从 A 到 B 多远、多久、开车/坐地铁要多少时间时用本步，不要用 query.content 编造距离。

## 典型触发语

- 从哪到哪开车多久
- 开车要多远
- 坐地铁需要多久
- 多远
- 多久能到
- 导航
- 路线
- 通勤时间

## 不要派给它

- 知识百科
- 看图
- 拍照
- 投屏
- 报时
- 闲聊

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `city` | string | 否 | 城市名，用于地址消歧与公交规划，默认北京 |
| `destination` | string | 是 | 终点地名或地址，如「顺义建邦顺颐府」 |
| `mode` | string | 否 | 出行方式：driving（驾车，默认）\| transit（公交地铁）\| walking（步行） |
| `origin` | string | 是 | 起点地名或地址，如「望新花园」 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 给人听/看的路线距离与耗时摘要 |
| `distance_km` | string | 是 | 路线距离（公里，小数） |
| `distance_m` | string | 否 | 路线距离（米） |
| `duration_min` | string | 是 | 预计耗时（分钟，向上取整） |
| `duration_sec` | string | 否 | 预计耗时（秒） |
| `mode` | string | 否 | 实际使用的出行方式 driving \| transit \| walking |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| Brain | `system` | `system.map` |

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
