# Script to do post-process
#   1.  Read file from Person-detection software
#   2.  Read file from Ultrasonic Measurement software
#   3.  Extract timestamp (file created) from both files
#   4.  Normally timestamps in person-detection will be longer and cover all of timestamps in ultrasonic file
#       Then extract only the intersect timestamp from person-detection.
#   5.  Get label_cams for timestamp and export label_cams as txt file.




def export_data(path, data):
    with open(path, 'w') as f:
        for line in data:
            f.write(line)


import os
import time

from os.path import join
from datetime import datetime, timedelta
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

cam_timestamps = []
label_cam = []
# Get timestamps for Camera data
for str in data_cam:
    split_str =  str.split(' : ')
    timestring = split_str[0]
    
    label_res = split_str[1]
    # label_res = label_res.split(r'\n')[0]
    
    label_cam.append(label_res)
    e = datetime.strptime(timestring, datetime_format)
    timestamp = datetime.timestamp(e)
    cam_timestamps.append(timestamp)

# Add timestmamps for ultrasonic data 
data_ultra_timestamps = []
u_basetime = datetime.fromtimestamp(u_time)
plus_time = timedelta(seconds=1)
for i in range(len(data_ultra)):
    if i == 0:
        e = u_basetime
    elif i % sec_per_measurement == 0:
        e = e + plus_time
        
    timestamp = datetime.timestamp(e)
    data_ultra_timestamps.append(timestamp)
    
# Compare and extract the same timestamps between two data
unique_ultra_timestamp = np.unique(data_ultra_timestamps)

keyword_PER = "person"
keyword_EMP = "Empty"
for ultra_ts in unique_ultra_timestamp:
   
    ultra_ts_index = data_ultra_timestamps.index(ultra_ts)
    
    # Extract index for same timestamps between both
    res_idx = []
    for cam_ts in cam_timestamps:
        if cam_ts == ultra_ts:
            res_idx.append(cam_timestamps.index(cam_ts))
    
    if res_idx == []:
        continue
    
    # Extract prediction result
    data_export = []
    res_list = []
    for idx in res_idx:
        res_list.append(label_cam[idx])
    
    cnt_person = sum(keyword_PER in s for s in res_list)    
    cnt_empty  = sum(keyword_EMP in s for s in res_list)
    
    if cnt_person > cnt_empty:
        res_percent = cnt_person * 100/ len(res_list)
        pred_res = "person"
    else:
        res_percent = cnt_empty * 100/ len(res_list)
        pred_res = "empty"
        
    date_time = datetime.fromtimestamp(ultra_ts)
    datetime_str = date_time.strftime(datetime_format)    
    
    
    print(datetime_str+" prediction result : "+pred_res+" with the percentage = ", res_percent)        
    
    # If the results are certain (100 percent), then collect data from ultrasonic sensor
    
    if res_percent == 100.0:     
        data_export = data_ultra[ultra_ts_index:ultra_ts_index + sec_per_measurement]
        filename = datetime_str+'.txt'
        filename = filename.replace(":", ".")
        filename = filename.replace("/", "-")
        
        export_data(filename, data_export)
        print("export data to file") 
        
        
        
# Majority vote to decide each second prediction

print("End of process")

