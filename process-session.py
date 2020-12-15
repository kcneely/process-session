##Process Virtual Whatsapp Sessions##
##Version 2020-12-09##
##by Kelsey C. Neely##

##This script takes a folder of .ogg audio files (e.g., audio downloaded from WhatsApp) and uses ffmpeg to convert them to .wav files corresponding to each clip and concatenate them to a "master" .wav file of the entire session. When this processing is complete, it deletes (permanently!) the .ogg files.

##Step 1: make sure you have python *and* ffmpeg installed, and save a back-up copy of the session files in case something goes wrong!
##Step 2: in command line, set current directory to path of folder where session files are located using the change directory command, e.g.: 
## cd C:\Users\kelsey\Desktop\KCN-20201112
##Step 3: copy and paste this .py file into that folder, then run it from the command line, e.g.:
## py process-session.py
##Step 4: check that you have the same number of .wav files as there were original .ogg files, check the concatenated file "Success.wav" to make sure the process was actually successful
##Step 5: rename the file Success.wav to match your project's filenaming conventions

import glob
import os
from datetime import datetime
import subprocess

##strip prefixes from filenames##
files = glob.glob('*.ogg')
for file in files:
    original_name = os.path.basename(file)
    if original_name.startswith("WhatsApp Audio"):
        os.rename(original_name, original_name[15:])
    else: 
        os.rename(original_name, original_name[13:])

##rename files to YYYY-MM-DD_HH-MM-SS format##
files = glob.glob('*.ogg')
for file in files:
    stripped_name = os.path.basename(file)
    date_object = datetime.strptime(stripped_name, "%Y-%m-%d at %I.%M.%S %p.ogg")
    final_name = datetime.strftime(date_object, "%Y-%m-%d_%H-%M-%S.ogg")
    os.rename(stripped_name, final_name)

##call ffmpeg to reencode individual ogg to wav##
files = glob.glob('*.ogg')
for file in files:
    name = ''.join(file.split('.')[:-1])
    output = '{}.wav'.format(name)
    reencode = 'ffmpeg -i {} {}'.format(file, output)
    subprocess.call(reencode)

##create file listing##
names = [os.path.basename(x) for x in glob.glob('*.wav')]
names = map(lambda x: 'file \'' + x + '\'\n', names)
with open('output.txt', "w") as a:
    a.writelines(names)

##call ffmpeg to concatenate multiple wav to single wav##
filelist = 'output.txt'
output = 'Success.wav'
concatenate = 'ffmpeg -f concat -safe 0 -i {} {}'.format(filelist, output)
subprocess.call(concatenate)

##delete ogg files##
files = glob.glob('*.ogg')
for file in files:
    os.remove(file)