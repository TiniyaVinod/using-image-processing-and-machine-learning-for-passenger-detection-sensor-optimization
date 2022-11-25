import tkinter as tk
from datetime import datetime
from os.path import exists, join, splitext

import cv2
import numpy as np
from PIL import Image, ImageTk
from timeit import default_timer as timer

from app_gui import app_gui
from model_class import model_class
from common_functions import read_config
from program_mode import *
import json
from datetime import datetime


# --- main ---

global cap, run_camera, global_frame, roi_points, roi_img, isconnect_cam
roi_flag = False
run_camera = False
window_app_run = False
isconnect_cam = False
status_text = ""
roi_points = []
config_filename = "config.json"

if not exists(config_filename):
    print('Cannot find configuration file')
    
config = read_config(config_filename)

model_filename = config["model_classification"]['model_filename']
device = config["model_classification"]['computing_device']

# create window application
window_app = tk.Tk()
config_gui = config['gui_prop']
window_app.title(config_gui['window_title'])
window_app.geometry = (config_gui['window_geometry'])
window_app.resizable(width=False, height=False)

canvas_w = config_gui['canvas_width']
canvas_h = config_gui['canvas_height']

# first frame with clear white image and init filter_image
white_img = np.zeros([canvas_w, canvas_h, 3], dtype=np.uint8)
roi_img = white_img.copy()
white_img.fill(255) 
roi_img.fill(0)

default_img = Image.fromarray(white_img)
default_img = ImageTk.PhotoImage(default_img) 

default_img2 = Image.fromarray(white_img)
default_img2 = ImageTk.PhotoImage(default_img2) 
global_frame = white_img

model = model_class(config["model_classification"])

if not window_app_run:
    window_app_run = True
    gui = app_gui(
        window_app, 
        default_img, 
        default_img2, 
        canvas_w, 
        canvas_h,
        config
        )

# Button Functions ----------------------------------------------------------
def connect_cam():
    global cap, video_writer, isconnect_cam
    
    if isconnect_cam:
        return 0
    
    # Check current selected tab
    select_mode = gui.gui_down.get_select_mode()
    record_status = gui.gui_down.get_record_status()
    
    cam_num = gui.gui_down.get_camera_number()
    video_path = gui.gui_down.get_video_path()
    
    # Check mode
    cam_mode = (select_mode == 0) & (record_status == 0)
    vid_mode = (select_mode == 1)
    
    
    # Behave according to mode
    if cam_mode: # CAMERA    
        [cap, msg] = realtime_mode(cam_num)
                
    elif vid_mode: # VIDEO
        [cap, msg] = video_mode(video_path)
        
    else:   # Auto Mode ( Not implemented )
        return 0
    
    display_status(msg)
    if cap == 0:
        stop()
        return 0
    
    isconnect_cam = True
    
    button_play['state'] = 'normal'
    button_stop['state'] = 'disabled'
    button_connectcam['state'] = 'disabled'
    button_disconnectcam['state'] = 'normal'
    
def disconnect_cam():
    
    global isconnect_cam
    
    if isconnect_cam:
        cap.release()
        isconnect_cam = False
    else:
        return 0
    
    display_status("STATUS: Camera inactive")
    
    isconnect_cam = False

    button_play['state'] = 'disabled'
    button_stop['state'] = 'disabled'
    button_connectcam['state'] = 'normal'
    button_disconnectcam['state'] = 'disabled'
    
def play():
    '''
    start_timer stream (run_camera and update_image) 
    and change state of buttons_left
    '''
    global cap, run_camera, record_result, video_writer
    
    record_result = []
    rec_mode = gui.gui_down.get_record_status()
        
    # Check if it is record mode
    if rec_mode:
        # Path to write record
        export_folder = config['export']['export_record_folder']
        export_filename = gui.gui_down.get_record_export_path()
        
        video_writer = record_mode(cap, export_folder, export_filename)
    
    if not run_camera:
        run_camera = True
        
        button_play['state'] = 'disabled'
        button_stop['state'] = 'normal'
        button_connectcam['state'] = 'disabled'
        button_disconnectcam['state'] = 'disabled'
        
        gui.gui_down.disable_setting()
        
        update_frame()
    
    # Clear Text
    if isconnect_cam == True:
        gui.gui_down.scroll_txt_left.config(state=tk.NORMAL)
        gui.gui_down.scroll_txt_left.delete('1.0', tk.END)
    
    
        
def stop():
    '''
    stop stream (run_camera) 
    and change state of buttons_left
    '''
    global run_camera, video_writer

    if isconnect_cam == False:
        return 0
    
    if run_camera:
        run_camera = False
    
    # if record mode is activated, release the object
    if gui.gui_down.get_record_status() == 1:
        video_writer.release()
        export_result()
    else:
        gui.gui_down.btn_record['state'] = 'normal'
   
    button_play['state'] = 'normal'
    button_stop['state'] = 'disabled'
    button_connectcam['state'] = 'disabled'
    button_disconnectcam['state'] = 'normal'
    
    gui.gui_down.enable_setting()
    
    display_status("STATUS : STOP Frame")

# Region of Interest functions--------------------------------------------------

def apply_ROI():
    global roi_flag, roi_points
    
    if roi_points:
        roi_flag = True
    else:
        display_status("STATUS : ROI points are not specified")
        roi_flag = False
    
def remove_ROI():
    global roi_flag
    roi_flag = False    

def default_roi(config):
    
    '''
    Set roi points to default
    '''
    
    global roi_points, roi_img
    
    roi_points = config['preprocess']['roi_points']
    
    # Connect dots and create polygon       
    pts = np.array(roi_points,np.int32)
    roi_img = cv2.fillPoly(roi_img, [pts], (255,255,255))
    
def draw_polygon_roi(frame):
    
    global roi_points
    
    # draw polygon if with the specified points
    if roi_points: # not empty
        pts = np.array(roi_points, np.int32)
        frame_roi = cv2.polylines(frame, [pts], isClosed = True, color = (255,0,0), thickness=1)
        
        return frame_roi
    else: # empty
        return frame
        
def preprocess_frame(frame):

    # Resize frame
    dim = (gui.canvas_w, gui.canvas_h)
    frame_resize = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    # Correct the color
    frame_corr_color = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2RGB)

    # Mirror horizontally
    frame_flip = np.fliplr(frame_corr_color)
        
    return frame_flip    

output_score = []

count = 0
chair_count = 0
non_chair_count = 0
person_count = 0
non_person_count = 0
def update_frame():
    start_timer = timer()
    
    global global_frame, roi_img, roi_flag, record_result
    
    # Read frame capture object
    ret, frame = cap.read()

    
    # font = cv2.FONT_HERSHEY_SIMPLEX
  
    # # org
    # org = (50, 50)
    
    # # fontScale
    # fontScale = 1
    
    # # Blue color in BGR
    # color = (255, 0, 0)
    
    # # Line thickness of 2 px
    # thickness = 2
    
    # # Using cv2.putText() method
    # frame = cv2.putText(frame, 'Person', org, font, 
    #                fontScale, color, thickness, cv2.LINE_AA)




    curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    
    datetime_format = "%m/%d/%Y, %H:%M:%S" # .f

     # If can't read frame
    if (ret is None) | (ret == False):
        display_status("STATUS : Cannot capture frame from source")
        stop()
        return 0
    
    frame_flip = preprocess_frame(frame)

    

    global_frame = frame_flip.copy()
    
    # Record Mode
    if gui.gui_down.get_record_status() == 1:
        video_writer.write(frame)
    
    # Apply ROI filter
    if roi_flag == True: 
        frame_show = frame_flip.copy()
        frame_show = draw_polygon_roi(frame_show)
        frame_flip[roi_img == 0] = 0 
        
    else:
        frame_show = frame_flip 
    

    img = Image.fromarray(frame_show)
    
    
    


    gui.gui_top.canvas_l_img.paste(img)
    
    select_mode = gui.gui_down.select_mode
    
    # Classification
    # Set parameter
    # model.model.conf = gui.gui_down.get_conf_thresh()
    predicted_result_from_model = model.predict_result(frame_flip)
    predictions = predicted_result_from_model[0]
    output_result_text = predicted_result_from_model[1]
    predictions_all_class = predicted_result_from_model[2]
    # print("Check predictions")
    # print(predictions, type(predictions))
    
    categories = predictions[:, 5]
    
    sec = cap.get(cv2.CAP_PROP_POS_MSEC)
    second = "{:.2f}".format(sec*0.001)
    
    person_classcode = 0.0
    pred_storage = list(predictions.storage())
    # print("pred_storage")
    # print(pred_storage)
    # print(dir(predictions))
    # print("-------------------------")
    boxes = []
    img_with_keypoints = frame_flip.copy()
    for obj in predictions_all_class:
        print("Predicion Label : ", obj)
        print("********************++++")
        x1 = int(obj["x1"])
        y1 = int(obj["y1"])
        x2 = int(obj["x2"])
        y2 = int(obj["y2"])
        label = obj["label"]
        confidence = obj["confidence"]
        text = f"{label.upper()} : {confidence} %"

        color_val = min(255, obj["label_int"]*3)
        box_color = (255, color_val, color_val)

        cv2.rectangle(img_with_keypoints, (x1, y1), (x2, y2), box_color, (1))
        cv2.putText(img_with_keypoints, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, box_color, 1)
    img2 = Image.fromarray(img_with_keypoints)
    # Check if there is any person in the frame  
    if False:
        # Find index of person
        x = pred_storage.index(person_classcode)
        
        score = pred_storage[x-1]
        boxes = pred_storage[x-5:x-1] # x1, y1, x2, y2
        
        img_with_keypoints = frame_flip.copy()

        try:
            x1 = int(boxes[0])
            y1 = int(boxes[1])
            x2 = int(boxes[2])
            y2 = int(boxes[3])
            
            # cv2.rectangle(img_with_keypoints, (x1, y1), (x2, y2), (0,255,0), (5))
            # cv2.putText(img_with_keypoints, 'person score: '+str(score), (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        except:
            print("boxes does not exist")
        
        img2 = Image.fromarray(img_with_keypoints)

        

        pred_result = "Person"
        text = form_predict_text(select_mode, second, datetime_format, pred_result)
        
    elif False:
        img2 = Image.fromarray(frame_flip)
        
        pred_result = "Empty Scence"
        text = form_predict_text(select_mode, second, datetime_format, pred_result)

    img_array = np.array(img2)
        
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (5, 25)
    # org2 = (5, 50)
    # org3 = (5, 75)
    # org4 = (5, 100)
    orgs = [(5, 25*(i+1)) for i in range(len(output_result_text))]
    # fontScale
    fontScale = 0.5
    
    # Blue color in BGR
    color = (255, 0, 0)
    
    # Line thickness of 2 px
    thickness = 1
    # Saving the prediction result of the program
    # for i in range(len(output_result_text)):
    #     img_array = cv2.putText(img_array, output_result_text[i], orgs[i], font, 
    #             fontScale, color, thickness, cv2.LINE_AA)
    # Using cv2.putText() method

    # img_array = plot_boxes(predictions_all_class, img_array)
    
    timestamp = (datetime.today()-datetime.today().replace(hour=0, minute=0, second=0)).seconds
    image_name = f'{timestamp}_'
    global chair_count
    global non_chair_count
    global person_count
    global non_person_count
    global count
    increase_chair_count = False
    # increase total_count
    count += 1
    local_chair_only_count = 0
    for i in range(len(output_result_text)):
        if ("CHAIR" in output_result_text[i] or "TOILET" in output_result_text[i] ) and "PERSON" not in output_result_text[i]:
            local_chair_only_count += 1
    
    if local_chair_only_count == len(output_result_text):
        increase_chair_count = True
        print("INCREASE CHAIR COUNT !!!!!!!!!!!!")

    output_label = ""

    if increase_chair_count:
        output_label = "chair"
        chair_count += 1
        image_name += f"{count}_chair_{chair_count}"
        increase_chair_count = False
    else:
        output_result = " ".join(output_result_text[:3])
        print(output_result, " JOINED RESULT")
        if "PERSON" in output_result:
            output_label = "person"
            person_count += 1
            image_name += f"{count}_person_{person_count}"
        else:
            output_label = "others"
            non_person_count += 1
            # image_name = f"{count}_non_person_{non_person_count}"
            non_chair_count += 1
            image_name += f"{count}_others_{non_chair_count}"
            increase_chair_count = False

    

    

    # true_positive = person_count
    # false_positive = 0
    # true_negative = 0
    # false_negative = non_person_count

    # precision = true_positive / (true_positive + false_positive)

    # recall = true_positive / (true_positive + false_negative)

    # f1_score = (2*precision*recall)/(precision + recall)

    global output_score
    # print(count, f1_score)
    # score_data = {
    #     "total_count": true_positive + false_negative + true_negative + false_positive,
    #     "true_positive": true_positive,
    #     "false_positive": false_positive,
    #     "true_negative": true_negative,
    #     "false_negative": false_negative,
    #     "precision": precision,
    #     "recall": recall,
    #     "f1_score": f1_score
    # }
    # score_data = {
    #     "total_count": count
    # }
    # predictions = []
    # for text in output_result_text:
    #     class_name = text.split(",")[0].split(":")[-1].strip()
    #     confidence_score = text.split(",")[1].split(":")[-1].strip()
    #     pred_dictionary = {
    #         class_name: confidence_score
    #     }
    #     predictions.insert(-1, pred_dictionary)
    # score_data["predictions"] = predictions
    # output_score.insert(0, score_data)

    predictions = {
        "total_count": count,
        "timestamp": timestamp,
        "prediction": output_label
    }

    output_score.insert(0, predictions)

    with open("prediction_result_2511_test1_with_timestamp.json", "w", encoding="utf-8") as f:
        json.dump(output_score, f, ensure_ascii=False, indent=4)


    

    # img_array = cv2.putText(img_array, output_result_text[1], org2, font, 
    #             fontScale, color, thickness, cv2.LINE_AA)

    img2 = Image.fromarray(img_array)

    if "chair" in image_name:
        img2.save(f"2511_test1_with_timestamp/frames_chair/{image_name}.jpg")
    elif 'person' in image_name:
        img2.save(f"2511_test1_with_timestamp/frames_person/{image_name}.jpg")
    else:
        img2.save(f"2511_test1_with_timestamp/frames_others/{image_name}.jpg")


    text = "some-text-value"

    # Save record result
    if gui.gui_down.get_record_status() == 1:
        record_result.append(text)
    
    gui.gui_down.display_scrolltext(text)
    gui.gui_top.canvas_r_img.paste(img2) 
    
    # Compute FPS
    sec_fps = timer()-start_timer
    fps = 1/sec_fps
    str_fps = "{:.2f}".format(fps)
    
    msg = "FPS : " + str_fps
    display_status(msg)
    
    if run_camera:
        window_app.after(10, update_frame)



def form_predict_text(select_mode, second, datetime_format, pred_result):
    if select_mode== 1:
        text = "Second : "+str(second)+" : "+pred_result
    else:
        dateTimeObj = datetime.now()
        text = dateTimeObj.strftime(datetime_format)+" : "+pred_result
    return text
    
def create_roi():
    
    global roi_points
    
    roi_points = []
    
    # Get Points from callback functions  
    cv2.imshow('ROI', global_frame)
    cv2.setMouseCallback('ROI', click_event_ROI)
    
def click_event_ROI(event, x, y, flags, params):

    global roi_img 
    
    roi_img = np.zeros([canvas_w, canvas_h, 3], dtype=np.uint8)
       
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        cv2.putText(global_frame, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        roi_points.append([x,y])
        cv2.imshow('ROI', global_frame)
        cv2.waitKey(0)
        cv2.destroyWindow('ROI')
        
        # Connect dots and create polygon       
        pts = np.array(roi_points,np.int32)
        roi_img = cv2.fillPoly(roi_img, [pts], (255,255,255))
    
def display_status(msg):
    status_text.config(text=msg)
    
def export_result():
    
    export_filename = splitext(gui.gui_down.get_record_export_path())[0]
    
    export_folder = config["export"]["export_record_folder"]
    export_filename = join(export_folder, export_filename+'.txt')
    
    with open(export_filename, 'w') as f:
        for line in record_result:
            f.write(line)
            f.write("\n")
        
# ---- buttons_left ----
buttons_left = tk.Frame(window_app)
buttons_left.grid(row=2, column=0)

button_play = tk.Button(buttons_left, text="Play", command=play, state='disabled')
button_play.pack(side='left')

button_stop = tk.Button(buttons_left, text="Stop", command=stop, state='disabled')
button_stop.pack(side='left')

button_connectcam = tk.Button(buttons_left, text="Connect Camera/Video", command=connect_cam)
button_connectcam.pack(side='left')

button_disconnectcam = tk.Button(buttons_left, text="Disconnect Camera/Video", command=disconnect_cam, state='disabled')
button_disconnectcam.pack(side='left')

# ---- buttons_right ----
buttons_right = tk.Frame(window_app)
buttons_right.grid(row=2, column=1)

button_apply_ROI     = tk.Button(buttons_right, text="Apply ROI", command=apply_ROI)
button_apply_ROI.pack(side='left')

button_default_ROI    = tk.Button(buttons_right, text="Remove ROI", command=remove_ROI)
button_default_ROI.pack(side='left')

button_create_ROI    = tk.Button(buttons_right, text="Create ROI", command=create_roi)
button_create_ROI.pack(side='left')

button_default_ROI    = tk.Button(buttons_right, text="default ROI", command=default_roi(config))
button_default_ROI.pack(side='left')


# ---- /end buttons_left ----

# Status Bar
status_text = tk.Label(window_app)
status_text.grid(row=3, column=0)

window_app.mainloop()