#!/usr/bin/env python3
from app_gui import app_gui
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
from os.path import exists
from blob_detector import *

# --- main ---

run_camera = False
window_app_run = False

backSub = cv2.createBackgroundSubtractorKNN()

# create window application
window_app = tk.Tk()
window_app.title("Person Detection")
window_app.geometry = ("1080x400")

canvas_w = 320
canvas_h = 320

# first frame with clear white image
white_img = np.zeros([canvas_w, canvas_h, 3], dtype=np.uint8)
white_img.fill(255) 
default_img = Image.fromarray(white_img)
default_img = ImageTk.PhotoImage(default_img) 

default_img2 = Image.fromarray(white_img)
default_img2 = ImageTk.PhotoImage(default_img2) 

if not window_app_run:
    window_app_run = True
    gui = app_gui(
        window_app, 
        default_img, 
        default_img2, 
        canvas_w, 
        canvas_h
        )

def play():
    '''
    start stream (run_camera and update_image) 
    and change state of buttons
    '''
    global cap, run_camera
    
    # Check current selected tab
    select_mode = gui.gui_down.get_select_mode()

    if (select_mode == 0): # CAMERA

        cam_no = gui.gui_down.get_camera_number()
        cap = cv2.VideoCapture(cam_no) # webcam : 0, other: 1

        # Check if source is accessible
        if not cap.isOpened():  
            cap.release()
            stop()
            return 0

    elif (select_mode == 1): # VIDEO
        video_path = gui.gui_down.get_video_path()

        if not exists(video_path):
            txt = "path [ "+video_path+" ] does not exist!"
            gui.gui_down.display_scrolltext(txt)
            stop()
            return 0
        else:
            cap = cv2.VideoCapture(video_path)   

    elif (select_mode == 2): # Record mode
        return 0
    else:   # Auto Mode
        return 0


    if not run_camera:
        run_camera = True
        
        button_play['state'] = 'disabled'
        button_stop['state'] = 'normal'
        button_pause['state'] = 'normal'
        button_resume['state'] = 'disabled'
        update_frame()
      
def stop():
    '''
    stop stream (run_camera) 
    and change state of buttons
    '''
    global run_camera

    if run_camera:
        run_camera = False

        cap.release()

    button_play['state'] = 'normal'
    button_stop['state'] = 'disabled'
    button_pause['state'] = 'disabled'
    button_resume['state'] = 'disabled'

def pause_frame():
    '''
    pause the stream
    and change state of buttons
    '''
    button_stop['state'] = 'normal'
    button_pause['state'] = 'disabled'
    button_resume['state'] = 'normal'

def resume_frame():
    '''
    resume the stream after pause
    and change state of buttons
    '''
    button_stop['state'] = 'normal'
    button_pause['state'] = 'normal'
    button_resume['state'] = 'diabled'

def preprocess_frame(frame):

    # Resize frame
    dim = (gui.canvas_w, gui.canvas_h)
    frame_resize = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    # Correct the color
    frame_corr_color = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2RGB)

    # Mirror horizontally
    frame_flip = np.fliplr(frame_corr_color)

    return frame_flip

def update_frame():

    ret, frame = cap.read()

     # If can't read frame
    if (ret is None) | (ret == False):
        stop()
        return 0

    frame_flip = preprocess_frame(frame)

    img = Image.fromarray(frame_flip)
    gui.gui_top.canvas_l_img.paste(img)

    frame_bg_sub = backSub.apply(frame_flip)
    # Select Method for Foreground detection
    if gui.gui_down.select_method == 0:
        # Background Subtraction 
        #frame_bg_sub = backSub.apply(frame_flip) # TODO uncomment this line

        # Filter only bg Sub part
        frame_filter = frame_flip
        frame_filter[frame_bg_sub==0] = 0

    elif gui.gui_down.select_method == 1:

        # Check if image path exist
        if not exists(gui.gui_down.get_bg_img_path()):
            txt = "Background image path does not exist!"
            gui.gui_down.display_scrolltext(txt)
            stop()
            return 0

        # TODO: Need to read only once, just a temporary solution 
        dim = (gui.canvas_w, gui.canvas_h)
        bg_img = cv2.imread(gui.gui_down.get_bg_img_path(), cv2.IMREAD_COLOR)
        bg_img = cv2.resize(bg_img, dim, interpolation = cv2.INTER_AREA)
        bg_img = np.fliplr(bg_img)

        # Absolute Diff
        frame_filter = cv2.cvtColor(frame_flip, cv2.COLOR_BGR2RGB)
        frame_sad = cv2.absdiff(frame_filter, bg_img)
        frame_filter[frame_sad<=40] = 0

    # Blob detection
    blob_keypoints = blob_detector.detect(frame_filter)
    if len(blob_keypoints) == 0:
        img2 = Image.fromarray(frame_filter)
        dateTimeObj = datetime.now()
        text = dateTimeObj.strftime("%m/%d/%Y, %H:%M:%S")+': Empty Scene'
        gui.gui_down.display_scrolltext(text)
    
    else:
        img_with_keypoints = cv2.drawKeypoints(
            frame_filter,
            blob_keypoints,
            np.array([]),
            (0,0,255),
            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        img2 = Image.fromarray(img_with_keypoints)
        dateTimeObj = datetime.now()
        text = dateTimeObj.strftime("%m/%d/%Y, %H:%M:%S")+': Human'
        gui.gui_down.display_scrolltext(text)
    
    gui.gui_top.canvas_r_img.paste(img2)
    
    if run_camera:
        window_app.after(10, update_frame)

# ---- buttons ----
buttons = tk.Frame(window_app)
buttons.grid(row=2)

button_play = tk.Button(buttons, text="Play", command=play)
button_play.pack(side='left')

button_stop = tk.Button(buttons, text="Stop", command=stop, state='disabled')
button_stop.pack(side='left')

button_pause = tk.Button(buttons, text="Pause", command=pause_frame, state='disabled')
button_pause.pack(side='left')

button_resume = tk.Button(buttons, text="Resume", command=resume_frame, state='disabled')
button_resume.pack(side='left')

# ---- /end buttons ----

blob_detector = init_blob_detector()

window_app.mainloop()

#cap.release()