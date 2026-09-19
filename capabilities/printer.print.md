# `printer.print`

米家喷墨一体机 · 文档打印机

kind=`output` · composition=`atomic` · group=`printer` · 声明=`是` · 在线=`是` · ℹ️ 实况与定义层不同（下列按实况）

## 规划器怎么认它

把本步已有的 PDF/document Asset 经本机 CUPS 队列打出纸。默认黑白（ColorModel=Gray）；彩打传 color_mode=color。入参 asset_ref（必填，type=document），可选 copies、printer_name、color_mode。不配网、不切 SoftAP、不走米家云

## 典型触发语

- 打印这份 PDF
- 把文档打出来
- 打印一下
- 打印这个文件
- 彩色打印

## 不要派给它

- 配网
- 切 SoftAP
- 扫描
- 投屏
- TTS
- 知识问答

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `asset_ref` | object | 是 | 必填 AssetRef JSON，type=document（PDF）。例 {"asset_id":"asset_…","type":"document"}。禁止 path / 永久 URL；缺则本能力无效。 |
| `color_mode` | string | 否 | bw（默认黑白）或 color（彩色） |
| `copies` | number | 否 | 份数，正整数，默认 1 |
| `printer_name` | string | 否 | 可选 CUPS 队列名；未传则用 MAC_EDGE_PRINTER_NAME，再否则匹配名含 Mi_All_in_One_Inkjet 的队列 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `color_mode` | string | 否 | 实际色彩：bw 或 color |
| `job_id` | string | 是 | CUPS 任务号，如 Queue-123 |
| `printer_name` | string | 是 | 实际使用的 CUPS 队列名 |
| `status_text` | string | 是 | 人类可读状态，如「已提交打印到 …」 |

## 谁提供

| 设备 | edge_id | 服务 |
|---|---|---|
| 客厅 · Mac Edge | `edge-node-IAtuhLSy` | `local.printer` |

## 服务声明

- `local.printer`

## 能力包

- `plugins/xiaomi-aio-printer/`

## 文档

- [home-agent-os/plugins/xiaomi-aio-printer/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/xiaomi-aio-printer/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/xiaomi_aio_printer.py`

## 相关配置

- `MAC_EDGE_PRINTER_NAME`

## 可用性

- 执行前探测（checker）：无
- 当前在线：是

- 定义层来源：`ads`、`package:xiaomi-aio-printer`、`service:local.printer`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `24d9217`），请勿手改。</sub>
