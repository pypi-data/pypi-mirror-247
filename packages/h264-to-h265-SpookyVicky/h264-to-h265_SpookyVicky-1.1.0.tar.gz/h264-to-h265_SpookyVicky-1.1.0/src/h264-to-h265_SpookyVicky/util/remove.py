import os
import ffmpeg
import sys
import colorama
import time
from util.db import db_save
from colorama import Back, Fore, Style
from os.path import join, getsize

def delete_all():
    

    rootfolder = input(Fore.CYAN + "folder path: ")
    print(Fore.GREEN + " Scanning... ")

    for root, dirs, files in os.walk(rootfolder):
        
        for name in files:
                
                if(name.split('.').pop() == 'mp4'):
                    video = os.path.join(root, name)
                    
                    metadata = ffmpeg.probe(video)
                    codec = metadata['streams'][0]['codec_name']
                    
                    if(codec == 'h264'):
                        print(Fore.RED + "Deleting " + name + "...")
                        os.remove(video)
                    else:
                        print(Fore.GREEN + "ignoring " + name + " [NOT H.264] " + codec)
    
    print(Fore.GREEN + "[ See you later :3 ]")

def delete_complete(tasklist):
    colorama.init(autoreset = True)
    for task in tasklist:
        if(task['status'] == True):
            try:
                print(Fore.RED + "Deleting " + task['name'] + "...")
                os.remove(task['path'])
            except:
                time.sleep(0.5)
                print(' \n UnU Bye Bye </3 ')
                break
    tasklist = []
    db_save(tasklist)            