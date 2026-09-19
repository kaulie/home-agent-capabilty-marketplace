# `music.recognize`

识曲（听歌识曲） · 识曲器（听歌识曲）

kind=`action` · composition=`atomic` · group=`music` · 声明=`是` · 执行前自检=`无`

## 规划器怎么认它

用户想听歌识曲时（打开识曲模式/这是什么歌/帮我听听），收录客厅 10~30 秒外放声音识别是哪首歌，输出一句话 answer_text（歌名）。只识别一首，命中或 30 秒超时结束。不是按歌名点播/暂停/切歌，不是读播放器正在播放的元数据

## 典型触发语

- 听歌识曲
- 帮我听一下这首歌
- 打开识曲模式
- 识别一下现在放的歌
- 这是什么歌

## 不要派给它

- 切歌
- 按歌名点播
- 播放音乐
- 暂停
- 知识问答
- 读 ncm 正在播放元数据
- 连蓝牙

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `max_sec` | number | 否 | 最长收录秒数，可选，默认环境值（≤60） |
| `min_sec` | number | 否 | 最短收录/首次识曲窗口秒数，可选，默认环境值 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `answer_text` | string | 是 | 给用户的一句话播报（歌名）；命中或超时都有 |
| `artist` | string | 否 | 歌手 |
| `confidence` | number | 否 | 置信度（可选） |
| `matched` | boolean | 否 | 是否识别成功 |
| `song_title` | string | 否 | 识别出的歌名 |

## 适用宿主（代码事实）

- `mac`

## 服务声明

- `music.recognize`

## 能力包

- `plugins/music-recognize/`

## 文档

- [home-agent-os/plugins/music-recognize/capability.md](https://github.com/kaulie/home-agent-os/blob/main/plugins/music-recognize/capability.md)

## 入口

- mac: `mac/src/mac_edge/plugins/music_recognize/__init__.py`

## 相关配置

- `MAC_EDGE_MUSIC_RECOGNIZE_ACR_ACCESS_KEY`
- `MAC_EDGE_MUSIC_RECOGNIZE_ACR_ACCESS_SECRET`
- `MAC_EDGE_MUSIC_RECOGNIZE_ACR_HOST`
- `MAC_EDGE_MUSIC_RECOGNIZE_AUDD_TOKEN`
- `MAC_EDGE_MUSIC_RECOGNIZE_MAX_SEC`
- `MAC_EDGE_MUSIC_RECOGNIZE_MIN_SEC`
- `MAC_EDGE_MUSIC_RECOGNIZE_PROVIDER`
- `MAC_EDGE_MUSIC_RECOGNIZE_RETRY_EVERY_SEC`
- `MAC_EDGE_MUSIC_RECOGNIZE_SHAZAM_HOST`
- `MAC_EDGE_MUSIC_RECOGNIZE_SHAZAM_KEY`


- 定义层来源：`ads`、`package:music-recognize`、`service:music.recognize`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
