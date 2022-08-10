# Script to do post-process
#   1.  Read file from Person-detection software
#   2.  Read file from Ultrasonic Measurement software
#   3.  Extract timestamp (file created) from both files
#   4.  Normally timestamps in person-detection will be longer and cover all of timestamps in ultrasonic file
#       Then extract only the intersect timestamp from person-detection.
#   5.  Get label_cams for timestamp and export label_cams as txt file.

import os
import time
import datetime
import numpy as np


sec_per_measurement = 10
datetime_format = "%m/%d/%Y, %H:%M:%S"
data_exclusion = 1


#   1.  Read file from Person-detection software
path_camera_file = r"../data/camera/Empty_scene_2.txt"
path_ultras_file = r"../data/ultrasonic/adc_Empty_scene_2_.txt"


# Both the variables would contain time
# elapsed since EPOCH in float
c_time = os.path.getctime(path_camera_file)
u_time = os.path.getctime(path_ultras_file)

tmp = int(u_time)
u_time = float(tmp)

# Converting the time in seconds to a timestamp
camera_basetime = time.ctime(c_time)
ultras_basetime = time.ctime(u_time)

print(c_time)
print(u_time)

data_cam = []
with open(path_camera_file) as f:
    data_cam = f.readlines()   
    
data_ultra = []
with open(path_ultras_file) as f:
    data_ultra = f.readlines()

data_cam_timestamps = []
label_cam = []
# Get timestamps for Camera data
for str in data_cam:
    split_str =  str.split(' : ')
    timestring = split_str[0]
    label_cam = split_str[1]
    e = datetime.datetime.strptime(timestring, datetime_format)
    timestamp = datetime.datetime.timestamp(e)
    data_cam_timestamps.append(timestamp)

# Add timestamps to ultrasonic data
data_ultra_timestamps = []
plus_time = 0
u_basetime = datetime.datetime.fromtimestamp(u_time)
e = u_basetime
plus_time = datetime.timedelta(seconds=1)
for i in range(len(data_ultra)):
    if i % sec_per_measurement == 0:
        e = e + plus_time
    
    timestamp = datetime.datetime.timestamp(e)
    data_ultra_timestamps.append(timestamp)
    
# Compare and extract the same timestamps between two data
# Only seconds matter
intersect_timelist = []
intersect_index = []

unique_ultra_timestamp = np.unique(data_ultra_timestamps)

for timestamp_cam in data_cam_timestamps:    
    for timestamp_ultra in data_ultra_timestamps:
      
        if timestamp_cam == timestamp_ultra:
            intersect_timelist.append(timestamp_cam)
            idx = data_cam_timestamps.index(timestamp_cam) 
            intersect_index.append(idx)

unique_intersect_idx = np.unique(intersect_index)

#for timestamp_ultra in data_ultra_timestamps:
    
 
    
    
    
    
    
               



print("End of process")




