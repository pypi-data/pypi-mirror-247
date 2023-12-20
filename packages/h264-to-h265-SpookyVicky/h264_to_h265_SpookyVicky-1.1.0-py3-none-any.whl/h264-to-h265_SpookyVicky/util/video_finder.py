import os
import ffmpeg
from os.path import join, getsize
from util.db import *
from colorama import Back, Fore, Style

def find_something():
    
    rootfolder = input(Fore.CYAN + "folder path: ")
    
    print(Fore.GREEN + " Scanning... ")

    for root, dirs, files in os.walk(rootfolder):
        
        for name in files:
                
                if(name.split('.').pop() == 'mp4'):
                    video = os.path.join(root, name)
                    print(video)
                    metadata = ffmpeg.probe(video)
                    codec = metadata['streams'][0]['codec_name']
                    
                    bit_rate = metadata['streams'][0]['bit_rate']
                    
                
                    audio_codec = metadata['streams'][1]['codec_name']
                    audio_bitrate = metadata['streams'][1]['bit_rate']
                    

                    if(codec == 'h264'):

                        out = os.path.join(root, "h265_" + name)
                        tasklist.append({
                         "name":name,
                         "path":video,
                         "out":out,
                         "bit_rate":bit_rate,
                         "audio_codec":audio_codec,
                         "audio_bitrate":audio_bitrate,
                         "status": False
                        })
    print(Fore.GREEN + " [ OK ] ")
    db_save(tasklist)
    return tasklist