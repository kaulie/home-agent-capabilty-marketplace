# 能力总表（mac edge）

> 由 `mac/scripts/export_capability_catalog.py` 从 home-agent-os `24d9217` 生成（2026-09-19T00:22:55Z）；**请勿手改** —— 改能力请改 home-agent-os 再跑 `scripts/sync.sh`。

## 概览

| 项 | 数 |
|---|---|
| 能力总数（并集） | 64 |
| 规划器广告定义（ADS） | 60 |
| 服务声明（services.py 静态） | 44（30 个 service） |
| 能力包（plugins/*/manifest.yaml） | 33 |
| **当前在线**（Brain 注册表） | 51 |
| ⚠️ 声明未上线 | 16 |
| ⚠️ 线上未声明 | 4 |
| 有执行前探测（checker） | 13 |

### 按 group

| group | 能力数 |
|---|---|
| `music` | 8 |
| `display` | 7 |
| `convert` | 5 |
| `camera` | 4 |
| `notify` | 4 |
| `reading` | 4 |
| `asset` | 2 |
| `bluetooth` | 2 |
| `game` | 2 |
| `network` | 2 |
| `vision` | 2 |
| `voice` | 2 |
| `aquarium` | 1 |
| `chat` | 1 |
| `climate` | 1 |
| `clock` | 1 |
| `document` | 1 |
| `experiment` | 1 |
| `light` | 1 |
| `lock` | 1 |
| `map` | 1 |
| `math` | 1 |
| `meta` | 1 |
| `ocr` | 1 |
| `phone` | 1 |
| `printer` | 1 |
| `pronunciation` | 1 |
| `query` | 1 |
| `read` | 1 |
| `search` | 1 |
| `video` | 1 |
| `visual` | 1 |

### 按 kind

| kind | 能力数 |
|---|---|
| `action` | 36 |
| `output` | 14 |
| `input` | 10 |
| `system` | 4 |

## 能力清单（按 group）

### `aquarium`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`aquarium.set`](capabilities/aquarium.set.md) | action | 鱼缸控制器｜- | 关鱼缸 | — |

### `asset`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`asset.inventory`](capabilities/asset.inventory.md) | system | Asset 盘点查询器｜Brain | 刚才的照片 | ✅ |
| [`asset.upload`](capabilities/asset.upload.md) | action | Asset 上传器｜客厅 · Mac Edge | 上传到图片服务器 | ✅ |

### `bluetooth`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`bluetooth.connect`](capabilities/bluetooth.connect.md) | action | 蓝牙音箱连接器｜- | 连上音箱 | — |
| [`bluetooth.disconnect`](capabilities/bluetooth.disconnect.md) | action | 蓝牙音箱断开器｜- | 断开蓝牙 | — |

### `camera`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`camera.capture`](capabilities/camera.capture.md) | input | 拍照执行器｜- | 拍一下 | — |
| [`camera.capture_and_upload`](capabilities/camera.capture_and_upload.md) | action | 拍照并上传器｜- | 把刚拍的照片传到图床 | — |
| [`camera.take_video`](capabilities/camera.take_video.md) | input | 短视频拍摄器｜- | 录一段视频 | — |
| [`take_video`](capabilities/take_video.md) | input | 短视频拍摄器｜- | 录一段视频 | — |

### `chat`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`chat.smalltalk`](capabilities/chat.smalltalk.md) | action | 闲聊问候回复器｜客厅 · Mac Edge | 你好啊 | ✅ |

### `climate`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`climate.set`](capabilities/climate.set.md) | action | 空调控制器｜客厅 · Mac Edge | 关掉空调 | ✅ |

### `clock`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`clock.now`](capabilities/clock.now.md) | input | 本机时钟读取器｜Brain | 今天几号 | ✅ |

### `convert`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`file.convert`](capabilities/file.convert.md) | action | 文件格式转换器｜客厅 · Mac Edge | 合成一个 PDF | ✅ |
| [`pdf.reader`](capabilities/pdf.reader.md) | action | PDF 语音朗读器｜客厅 · Mac Edge | 念一下这份 PDF | ✅ |
| [`pdf.rotate`](capabilities/pdf.rotate.md) | action | PDF 旋转器（横版/竖版）｜客厅 · Mac Edge | PDF 横竖切换 | ✅ |
| [`pdf.to_images`](capabilities/pdf.to_images.md) | action | PDF 页面渲染器｜客厅 · Mac Edge | PDF 转图片 | ✅ |
| [`web.scraper`](capabilities/web.scraper.md) | action | 网页抓取器（URL / url 资产 → 核心正文/整页 → PDF/文本）｜客厅 · Mac Edge | 保存这个网页 | ✅ |

### `display`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`display.audio`](capabilities/display.audio.md) | output | 音频投电视播放器｜客厅 · Mac Edge | 在电视上放这段音频 | ✅ |
| [`display.audio.control`](capabilities/display.audio.control.md) | output | 电视音频播放控制器｜客厅 · Mac Edge |  | ✅ |
| [`display.pdf`](capabilities/display.pdf.md) | output | PDF 投屏打开器｜客厅 · Mac Edge | PDF 上电视 | ✅ |
| [`display.pdf.page`](capabilities/display.pdf.page.md) | output | PDF 投屏翻页器｜客厅 · Mac Edge | 上一页 | ✅ |
| [`display.pdf.zoom`](capabilities/display.pdf.zoom.md) | output | PDF 投屏缩放器｜客厅 · Mac Edge | 放大一点 | ✅ |
| [`display.photo`](capabilities/display.photo.md) | output | 单图投屏器｜客厅 · Mac Edge | 丢到电视 | ✅ |
| [`display.slideshow`](capabilities/display.slideshow.md) | output | 多图幻灯片投屏器｜客厅 · Mac Edge | 把这些照片轮播 | ✅ |

### `document`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`document.scan`](capabilities/document.scan.md) | input | 纸质文档扫描器｜- | 扫一下 | — |

### `experiment`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`voice_test.run_trial`](capabilities/voice_test.run_trial.md) | action | 台灯语音控制实验器｜客厅 · Mac Edge | 测一下语音控制台灯 | ✅ |

### `game`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`game.input`](capabilities/game.input.md) | input | 游戏语音/手势输入｜- | 挥手玩游戏 | — |
| [`game.launch`](capabilities/game.launch.md) | output | 电视互动游戏启动器｜客厅 · Mac Edge | 启动游戏 | ✅ |

### `light`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`light.set`](capabilities/light.set.md) | action | 灯光控制器｜客厅 · Mac Edge | 亮一点 | ✅ |

### `lock`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`lock.status`](capabilities/lock.status.md) | input | 门锁状态读取器｜- | 门关了吗 | — |

### `map`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`map.route.estimate`](capabilities/map.route.estimate.md) | system | 路线距离与耗时查询器｜Brain |  | ✅ |

### `math`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`math.calculate`](capabilities/math.calculate.md) | action | 确定性算术求值器｜客厅 · Mac Edge | 1+1等于几 | ✅ |

### `meta`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`capabilities.summary`](capabilities/capabilities.summary.md) | system | 在线能力口语汇总器｜Brain | 你会什么 | ✅ |

### `music`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`music.cache`](capabilities/music.cache.md) | action | 音乐索引预取器｜客厅 · Mac Edge | 下载刘德华的歌 | ✅ |
| [`music.next`](capabilities/music.next.md) | action | 下一首切换器｜客厅 · Mac Edge | 下一首 | ✅ |
| [`music.pause`](capabilities/music.pause.md) | action | 暂停播放器｜客厅 · Mac Edge | 先停一下 | ✅ |
| [`music.play`](capabilities/music.play.md) | action | 音乐播放器｜客厅 · Mac Edge | 播放陈奕迅的十年 | ✅ |
| [`music.previous`](capabilities/music.previous.md) | action | 上一首切换器｜客厅 · Mac Edge | 上一曲 | ✅ |
| [`music.recognize`](capabilities/music.recognize.md) | action | 识曲器（听歌识曲）｜客厅 · Mac Edge | 听歌识曲 | ✅ |
| [`music.resume`](capabilities/music.resume.md) | action | 继续播放器｜客厅 · Mac Edge | 恢复播放 | ✅ |
| [`music.stop`](capabilities/music.stop.md) | action | 停止播放器｜客厅 · Mac Edge | 停止播放 | ✅ |

### `network`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`network.wifi.join`](capabilities/network.wifi.join.md) | action | 临时 Wi-Fi 调试连接器｜- | 加入指定 SSID | — |
| [`network.wifi.leave`](capabilities/network.wifi.leave.md) | action | 临时 Wi-Fi 调试断开器｜- | 回到家里默认网络 | — |

### `notify`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`notify.speak`](capabilities/notify.speak.md) | output | 语音播报器｜客厅 · Mac Edge | 一分钟后说 | ✅ |
| [`xiaodu.control`](capabilities/xiaodu.control.md) | output | 小度音箱播放控制器｜客厅 · Mac Edge |  | ✅ |
| [`xiaodu.play`](capabilities/xiaodu.play.md) | output | 小度音箱音频播放器｜客厅 · Mac Edge |  | ✅ |
| [`xiaodu.speak`](capabilities/xiaodu.speak.md) | output | 小度音箱播报器｜客厅 · Mac Edge | 客厅音箱说 | ✅ |

### `ocr`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`image.ocr`](capabilities/image.ocr.md) | system | 图片文字识别器｜Brain | OCR | ✅ |

### `phone`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`phone.call`](capabilities/phone.call.md) | action | 电话拨打器｜- | 打个电话 | — |

### `printer`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`printer.print`](capabilities/printer.print.md) | output | 文档打印机｜客厅 · Mac Edge | 彩色打印 | ✅ |

### `pronunciation`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`pronunciation.assess`](capabilities/pronunciation.assess.md) | action | 整段英文朗读评测器｜- | assess my reading | — |

### `query`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`query.content`](capabilities/query.content.md) | action | 文本知识与推理回答器｜客厅 · Mac Edge | 为什么天是蓝的 | ✅ |

### `read`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`paper.read`](capabilities/paper.read.md) | action | 论文听读器（论文/长文献 → 结构化听读音频）｜客厅 · Mac Edge | 听读这篇 paper | ✅ |

### `reading`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`reading.detect_finger`](capabilities/reading.detect_finger.md) | action | 食指检测器｜客厅 · Mac Edge | 指尖在哪 | ✅ |
| [`reading.ocr_at_finger`](capabilities/reading.ocr_at_finger.md) | action | 指尖附近文字识别器｜客厅 · Mac Edge | 识别指尖附近的字 | ✅ |
| [`reading.point_to_character`](capabilities/reading.point_to_character.md) | action | 指字认字器｜客厅 · Mac Edge | 手指指的是什么字 | ✅ |
| [`reading.rank_pointed`](capabilities/reading.rank_pointed.md) | action | 指字排序器｜客厅 · Mac Edge | 选出手指指向的字 | ✅ |

### `search`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`search.images`](capabilities/search.images.md) | action | 互联网实拍图检索器｜客厅 · Mac Edge | 找网上的实拍图 | ✅ |

### `video`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`video.live_stream`](capabilities/video.live_stream.md) | input | iPhone 实时视频流入口｜- | 开始直播 | — |

### `vision`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`vision.ask`](capabilities/vision.ask.md) | action | 看图问答器｜客厅 · Mac Edge | 图里有 | ✅ |
| [`vision.perceive`](capabilities/vision.perceive.md) | action | 视觉结构化感知器｜客厅 · Mac Edge | 客厅现在什么样 | ✅ |

### `visual`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`visual.input`](capabilities/visual.input.md) | input | 纸质文档扫描器｜- | 扫一下小票 | — |

### `voice`

| 能力 | kind | 角色 / 设备 | 触发语（示例） | 在线 |
|---|---|---|---|---|
| [`voice.stream`](capabilities/voice.stream.md) | input | 常驻语音流入口｜客厅 · Mac Edge | 对着麦克风说话 | ✅ |
| [`voicewakeup.echo`](capabilities/voicewakeup.echo.md) | output | 唤醒回声｜客厅 · Mac Edge | 系统内部唤醒回声（非用户指令） | ✅ |

## ⚠️ 声明未上线（定义有、此刻没广告）

多半是可用性门控：设备没连 / 依赖没装 / 凭证没配。**不是故障**，但要能一眼看到。

| 能力 | kind | 声明方 | 有 checker |
|---|---|---|---|
| [`aquarium.set`](capabilities/aquarium.set.md) | action | livingroom.aquarium | 否 |
| [`bluetooth.connect`](capabilities/bluetooth.connect.md) | action | (ADS) | 否 |
| [`bluetooth.disconnect`](capabilities/bluetooth.disconnect.md) | action | (ADS) | 否 |
| [`camera.capture`](capabilities/camera.capture.md) | input | gopro.camera | 是 |
| [`camera.capture_and_upload`](capabilities/camera.capture_and_upload.md) | action | gopro.camera | 是 |
| [`camera.take_video`](capabilities/camera.take_video.md) | input | (ADS) | 否 |
| [`document.scan`](capabilities/document.scan.md) | input | (ADS) | 否 |
| [`game.input`](capabilities/game.input.md) | input | (ADS) | 否 |
| [`lock.status`](capabilities/lock.status.md) | input | entry.lock | 否 |
| [`network.wifi.join`](capabilities/network.wifi.join.md) | action | (ADS) | 否 |
| [`network.wifi.leave`](capabilities/network.wifi.leave.md) | action | (ADS) | 否 |
| [`phone.call`](capabilities/phone.call.md) | action | (ADS) | 否 |
| [`pronunciation.assess`](capabilities/pronunciation.assess.md) | action | local.pronunciation | 否 |
| [`take_video`](capabilities/take_video.md) | input | (ADS) | 否 |
| [`video.live_stream`](capabilities/video.live_stream.md) | input | (ADS) | 否 |
| [`visual.input`](capabilities/visual.input.md) | input | (ADS) | 否 |

## ⚠️ 线上未声明（在跑但不在 mac ADS 里）

| 能力 | 设备 | 服务 |
|---|---|---|
| [`display.audio.control`](capabilities/display.audio.control.md) |  | `` |
| [`map.route.estimate`](capabilities/map.route.estimate.md) |  | `` |
| [`xiaodu.control`](capabilities/xiaodu.control.md) |  | `` |
| [`xiaodu.play`](capabilities/xiaodu.play.md) |  | `` |

---

`home-agent.capability-catalog/v1`

