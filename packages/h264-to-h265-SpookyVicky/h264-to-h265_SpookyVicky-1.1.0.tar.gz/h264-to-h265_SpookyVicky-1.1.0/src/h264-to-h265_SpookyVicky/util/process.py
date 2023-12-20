import os
import ffmpeg
from os.path import join, getsize
from util.db import *
import time
from colorama import Back, Fore, Style

VIDEO_CODEC = 'hevc_qsv' #libx265 for CPU, hevc_nvenc for Nvidia GPU, hevc_qsv intel

def transcod(video, out, new_bitrate, audio_codec, audio_bitrate):
    
    (
    ffmpeg
    .input(video)
    .output(out, **{'b:v': new_bitrate, 'codec:v':VIDEO_CODEC, 'preset': 'slow', 'b:a':audio_bitrate, 'codec:a': audio_codec})
    .run()
    )
    print(Fore.GREEN + "[ OK ]")


def process(tasklist):

    for task in tasklist:
        if(task['status'] == False):
            print( Fore.MAGENTA + "transcoding " + task['name'])
            new_bitrate = int(float(task['bit_rate']) * .60) #60%
            try:
                transcod(task['path'], task['out'], new_bitrate, task['audio_codec'], task['audio_bitrate'])
                task['status'] = True
            except:
                time.sleep(0.5)
                os.remove(task['out'])
                print( Fore.CYAN + ' \n UnU Bye Bye </3 ')
                break
    db_save(tasklist)