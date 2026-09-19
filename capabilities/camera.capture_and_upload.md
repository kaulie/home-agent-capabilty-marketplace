# `camera.capture_and_upload`

拍照并上传器

kind=`action` · composition=`composite` · group=`-` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

拍一张现场照并在同一台设备上上传成 Image Asset，产出 asset_ref。拍照后还要给人看、给视觉问、投电视时优先本步，不要再拆成拍照+上传两步（capture_ref 不能跨机）。本步不负责看图理解、不投屏

> 优先本能力：拍照后还有后续动作要消费这张照片（给人看、变成 Asset、vision、投屏）时，优先本能力，不要把 decomposes_to 拆成多步

## 典型触发语

- 把刚拍的照片传到图床
- 拍张照片我看一下
- 拍张照片我看看
- 拍照后上传
- 拍的给我看

## 不要派给它

- 不再拍照只传旧图
- 只上传已有图
- 投屏本身
- 看图理解本身

## 分解为（接线图）

- `asset.upload`
- `camera.capture`

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dest` | string | 否 | img_server（默认）\| cloud。传给内部 asset.upload。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | 上传后的 AssetRef JSON。禁止 photo_url / path / capture_ref 当用户可见 identity。 |
| `dest` | string | 否 | img_server 或 cloud |

## 服务声明

- `gopro.camera`


- 定义层来源：`ads`、`service:gopro.camera`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
