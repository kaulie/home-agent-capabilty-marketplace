# `music.cache`

音乐索引预取器

kind=`action` · composition=`atomic` · group=`-` · 声明=`是` · 执行前自检=`有`

## 规划器怎么认它

闲时把歌名/歌手搜索结果写入本机索引，不播放、不下载音频。入参 song/artist，可选 count（1–200，默认 100）、fetch_audio（本轮忽略）。用户说「下载/缓存xxx的歌」用本步，不是 music.play

## 典型触发语

- 下载刘德华的歌
- 下载刘德华的歌50首
- 缓存歌曲冰雨

## 不要派给它

- TTS
- 下载音频文件
- 开始播放
- 暂停
- 蓝牙连接

## 入参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artist` | string | 否 | 歌手 |
| `count` | number | 否 | 预取条数，1–200，默认 100 |
| `fetch_audio` | boolean | 否 | 本轮忽略；true 时仍只写索引并说明未下载音频 |
| `song` | string | 否 | 歌名或「xxx的歌/歌曲」 |

## 出参

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `cached` | number | 否 | 本次写入索引的歌曲数 |

## 服务声明

- `netease.music`


- 定义层来源：`ads`、`service:netease.music`

---

<sub>由 `mac/scripts/export_capability_catalog.py` 生成（home-agent-os `5dc6531`），请勿手改。</sub>
