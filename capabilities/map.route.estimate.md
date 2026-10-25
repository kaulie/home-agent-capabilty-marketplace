# `map.route.estimate`

路线距离与耗时查询器

kind=`system` · composition=`atomic` · group=`map` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

查两地之间的驾车/公交地铁/步行距离与预计耗时，基于高德地图实时路网。入参 origin、destination 必填；mode 可选 driving|transit|walking（默认 driving）。assigned_edge_id=system。产出 answer_text、distance_km、duration_min。用户问从 A 到 B 多远、多久、开车/坐地铁要多少时间时用本步，不要用 query.content 编造距离。

## 典型触发语

- 从哪到哪开车多久
- 坐地铁需要多久
- 多久能到
- 多远
- 导航
- 开车要多远
- 路线
- 通勤时间

## 不要派给它

- 投屏
- 报时
- 拍照
- 看图
- 知识百科
- 闲聊

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `city` | string | 否 | 城市，用于消歧与公交规划，默认北京 |
| `destination` | string | 是 | 终点地名或地址 |
| `mode` | string | 否 | driving \| transit \| walking，默认 driving |
| `origin` | string | 是 | 起点地名或地址 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 口语化距离与耗时摘要 |
| `distance_km` | string | 是 | 距离（公里） |
| `duration_min` | string | 是 | 预计耗时（分钟） |

## 适用宿主（代码事实）

- `brain`

## 服务声明

- `system.map`


---

<sub>由 `scripts/export_catalog.py` 生成（marketplace `62e850e`），请勿手改。</sub>
