# h264 to h265 simple recursive transcoder❤

This is simple, you give the path to a parent folder and this will convert all '.mp4 (h264)' videos to '.mp4 (h265)' using only 60% of the original bitrate. If a video has already been converted or has an 'h265' codec it will be ignored

> normally h265 allows you to save 40% of the total bitrate maintaining an acceptable quality, although of course, if you want you could specify the bitrate to be used in line 43❤

## requirements

`'ffmpeg-python'`
> don't confuse it with python-ffmpeg  

## Note

If you use the CPU to encode, make sure you use libx265 and not hvec_nvenc (nvidia only)

`VIDEO_CODEC = 'libx265'`
