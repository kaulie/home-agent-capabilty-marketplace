# `vision.perceive`

Local Vision · 视觉结构化感知器

kind=`action` · composition=`atomic` · group=`vision` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

看已经有的 Image Asset，描述客厅现在什么样（人、灯、杂物）。入参 $asset_ref。自己不拍照：现场图要先拍再上传。不负责认剧名、不投屏、不开放百科问答

## 典型触发语

- 客厅现在什么样
- 描述一下画面
- 现在怎样
- 看看客厅
- 看看客厅现在怎样

## 不要派给它

- 开放问答
- 投屏
- 拍照本身
- 认电视剧名

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | AssetRef JSON {asset_id, type, mime_type?}。禁止 photo_url / path / 永久 URL。常为 $asset_ref。 |
| `prompt` | string | 否 | 可选额外提示 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `actions` | string | 否 | 主要动作 |
| `lighting` | string | 否 | 光线 JSON（whole + region） |
| `people` | string | 否 | 人物列表 JSON |
| `posture` | string | 否 | 体态/姿势 |
| `spatial` | string | 否 | 空间布局描述 |
| `summary` | string | 是 | 一句话画面摘要 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `local.vision`

## 能力包

- `plugins/vision-perceive/`

## 文档

- [home-agent-os/plugins/vision-perceive/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/vision-perceive/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/vision_perceive.py`


- 定义层来源：`ads`、`package:vision-perceive`、`service:local.vision`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
