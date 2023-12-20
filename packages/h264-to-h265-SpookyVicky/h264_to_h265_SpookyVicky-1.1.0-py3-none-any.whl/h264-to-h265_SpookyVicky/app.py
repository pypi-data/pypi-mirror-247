import os
import ffmpeg
import sys
from os.path import join, getsize
from util.db import *
from util.process import *
from util.video_finder import find_something
from util.remove import *
from colorama import Back, Fore, Style

def main():
    
    tasklist = db_load()
    
    if(tasklist):
        
        if(input( Fore.CYAN + 'continue from the last session?(Y/N)').lower() =='y' ):
            opt = input(Fore.CYAN + '[p]rocess or [d]elete h264 videos?').lower()
            if(opt == 'p'):
                process(tasklist)
            elif(opt == 'd'):
                delete_complete(tasklist)
        else:
            opt = input(Fore.CYAN + '[p]rocess or [d]elete h264 videos?').lower()
            if(opt == 'p'):
                tasklist = find_something()
                process(tasklist)
            elif(opt == 'd'):
                delete_all()
    else:
        opt = input(Fore.CYAN + '[p]rocess or [d]elete h264 videos?').lower()
        if(opt == 'p'):
            tasklist = find_something()
            process(tasklist)
        elif(opt == 'd'):
            delete_all()
main()

