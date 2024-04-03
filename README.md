## 离线m3u8及其视频分片文件合成mp4
* 使用方法  
1. 视频的`m3u8`文件需要与其对应的包含有切片的数据文件夹在同一目录，该目录这里描述为`m3u8_contents`文件夹
2. 一般情况下，`m3u8`文件名与其`m3u8_contents`文件夹名字相同
3. 使用`ffmpeg`指令进行合成，文件名中的`空格`，`(`，`)`不支持，会将其替换

```
usage: m3u8ToMp4.py [-h] [--mod {fix,convert,restore}] [--content-dir CONTENT_DIR] [--save-dir SAVE_DIR] [--encode-audio] m3u8_dir

Convert offline m3u8 to mp4

positional arguments:
  m3u8_dir              offline m3u8 file and content dir

options:
  -h, --help            show this help message and exit
  --mod {fix,convert,restore}
                        fix is fix m3u8 file path, convert is convert the m3u8 offline files to mp4, restore mod is restore the org m3u8 file
  --content-dir CONTENT_DIR
                        m3u8 content dir
  --save-dir SAVE_DIR   mp4 file save dir
  --encode-audio        enable encode audio
``` 

例如：
```sh
python m3u8ToMp4.py ./video --mod convert --encode_audio
```