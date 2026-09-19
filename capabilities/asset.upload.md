# `asset.upload`

Asset 上传器

kind=`action` · composition=`atomic` · group=`-` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

不负责按快门。把本机 inbox 的 capture 或已有 Asset 传到家里图床/云端，产出可给后续步用的 asset_ref。拍完要给人看、给视觉问、投电视，必须另排本步，入参 $capture_ref。已有 Asset 再传一份用 asset_ref

## 典型触发语

- 上传到图片服务器
- 传到家里图床
- 把刚拍的照片传到图床
- 把这张图传到云上
- 拍照后上传

## 不要派给它

- Dropbox
- Google Drive
- 投屏
- 拍照
- 看图理解

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 否 | 已登记 Asset 的 AssetRef JSON。禁止 photo_url / path / 永久 URL。已有 Asset 再传一份时用。 |
| `capture_ref` | string | 否 | 本机 inbox CaptureRef JSON {capture_id, type, mime_type}。拍照后上传常为 $capture_ref。 |
| `dest` | string | 否 | img_server（默认，本机图床）\| cloud \| gdrive \| dropbox。别名 lan/local/home → img_server。gdrive/dropbox 本轮未实现，必须失败。 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | string | 是 | 上传后的 AssetRef JSON。禁止 photo_url。 |
| `dest` | string | 是 | 实际写入的 dest：img_server 或 cloud |

## 服务声明

- `local.asset`


- 定义层来源：`ads`、`service:local.asset`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
