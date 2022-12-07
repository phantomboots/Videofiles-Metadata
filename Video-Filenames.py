###################################################################
# Generates list of video filenames with start and end times
#
# Author: Jessica Nephin (jessica.nephin@dfo-mpo.gc.ca)
# Nov 2022
#
# Requirements:
#   Requires ffmpeg command line tool to capture images,
#   Download at https://ffmpeg.org/
#   Python version 3.9.12
#
# Description:
#   1) Creates lists of video files names
#   2) Adds metadata fields: start and end time of videos
#
# Instructions:
#   1) Check that all required modules are installed
#   2) Modify inputs section below as needed
#   3) Check to make sure path to video files does not contain spaces!

###################################################################


###################################################################
#   Required modules
###################################################################

import os
import subprocess
import pandas as pd
import re


###################################################################
#   Inputs
###################################################################


# Folder name with videos, full path if not within current wd
# filenames must be tripID_diveID_YYYYMMMDD_HHMMSS or
# tripID_diveID_overlaid_YYYYMMMDD_HHMMSS
# No other files can be in this folder
videopath = 'Z:/Survey_Data/PAC2022-036_Vector_MPAs/HD_Recorder_MiniZeus/Overlaid'

# Location to store videofile list and metadata
outputpath = 'Z:/Survey_Data/PAC2022-036_Vector_MPAs/HD_Recorder_MiniZeus'


###################################################################
#   Video filenames
# ###################################################################

# List video files
videofiles = os.listdir(videopath)

# Empty lists to fill
f = []
s = []
e = []

 # Loop through each video file
for video in videofiles:

    # Parse video filename
    parts = video.split('_')
    tripid = parts[0]
    divename = parts[1]
    if parts[2] =='overlaid':
        videostart = parts[3] + '_' + parts[4].split('.')[0]
    else:
        videostart = parts[2] + '_' + parts[3].split('.')[0]
    
     # Format start datetime of video
    videoStartDateTime = pd.to_datetime(videostart, format='%Y%m%d_%H%M%S')
    
    # Get duration of video file in seconds, add a one second buffer
    durcall = ('ffprobe -v error -show_entries format=duration ' + videopath + '/' + video )
    durproc = subprocess.run(durcall, shell=True, capture_output=True, text=True)
    dur = float(re.sub('[^0-9.]', '', durproc.stdout)) + 1

    # Calculate datetime at end of video clip
    videoEndDateTime = videoStartDateTime + pd.Timedelta(seconds=int(dur))

    # Append to lists
    f.append(video)
    s.append(videoStartDateTime.strftime('%Y%m%dT%H%M%SZ') )
    e.append(videoEndDateTime.strftime('%Y%m%dT%H%M%SZ') )
    
# Create dataframe
d = pd.DataFrame()
d['Filename'] = f
d['Start_Datetime'] = s
d['End_Datetime'] = e

# Export path
efile = outputpath + '/' +tripid + '_VideoFilenames_Metadata.csv'
# Write csv
d.to_csv(efile) 
