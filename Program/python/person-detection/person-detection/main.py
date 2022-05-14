#!/usr/bin/env python3
from app_gui import app_gui
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime
from os.path import exists

def play():
    '''
    start stream (run_camera and update_image) 
    and change state of buttons
    '''
    global cap, run_camera

    video_path = gui.getVideoPath()

    # Check current selected tab
    select_tab = gui.getSelectedTab()

    if (select_tab == "video"):
        if not exists(video_path):
            txt = "path [ "+video_path+" ] does not exist!"
            gui.display_scrolltext(txt)
            exit(0) 
        else:
            cap = cv2.VideoCapture(video_path)   
    else:
        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture("videos/Person_sitandmove.mp4")
        #cap = cv2.VideoCapture(0)

        # Check if source is accessible
        if not cap.isOpened():  
            cap.release()
            stop()


    if not run_camera:
        run_camera = True
        
        button_play['state'] = 'disabled'
        button_stop['state'] = 'normal'
        update_frame()
      
def stop():
    '''
    stop stream (run_camera) 
    and change state of buttons
    '''

    if run_camera:
        run_camera = False

        cap.release()

        button_play['state'] = 'normal'
        button_stop['state'] = 'disabled'

def click_event(event, x, y):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        gui.display_scrolltext("select position (x,y) :", x,", ", y)

def init_blob_detector():
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 1
    params.maxThreshold = 255
    params.filterByArea = True
    params.minArea = 5000
    params.maxArea = 30000
    params.filterByCircularity = False
    params.minCircularity = 0.5
    params.filterByInertia = False
    params.filterByConvexity = False
    params.minConvexity = 0.95
    params.maxConvexity = 1e37
    params.filterByColor = True
    params.blobColor = 255
    detector = cv2.SimpleBlobDetector_create(params)
    return detector 

def update_frame():

    ret, frame = cap.read()

     # If can't read frame
    if (ret is None) | (ret == False):
        cap.release()

    # Resize frame
    dim = (gui.canvas_w, gui.canvas_h)
    frame_resize = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    # Correct the color
    frame_corr_color = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2RGB)

    # Mirror horizontally
    frame_flip = np.fliplr(frame_corr_color)
    
    img = Image.fromarray(frame_flip)
    gui.canvas_l_img.paste(img)

    # Background subtraction
    bgSubFrame = backSub.apply(frame_flip)

    # Blob detection
    blob_keypoints = blob_detector.detect(bgSubFrame)
    if len(blob_keypoints) == 0:
        img2 = Image.fromarray(bgSubFrame)
        text = dateTimeObj.strftime("%m/%d/%Y, %H:%M:%S")+': Empty Scene'
        gui.display_scrolltext(text)
    
    else:
        img_with_keypoints = cv2.drawKeypoints(
            bgSubFrame,
            blob_keypoints,
            np.array([]),
            (0,0,255),
            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        img2 = Image.fromarray(img_with_keypoints)
        text = dateTimeObj.strftime("%m/%d/%Y, %H:%M:%S")+': Human'
        gui.display_scrolltext(text)
    
    gui.canvas_r_img.paste(img2)
    
    if run_camera:
        window_app.after(10, update_frame)

# --- main ---

run_camera = False
bgSubFlag = False
ROI_Flag = False
window_app_run = False

backSub = cv2.createBackgroundSubtractorKNN()

blob_detector = init_blob_detector()

dateTimeObj = datetime.now()

# --- main ---

#cap = cv2.VideoCapture("videos/Person_stand.mp4")
#cap = cv2.VideoCapture("videos/Empty_scene+chair_2.mp4")

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
    
    #gui.init_gui()


# ---- buttons ----
buttons = tk.Frame(window_app)
buttons.pack(side='bottom', fill='x')

button_play = tk.Button(buttons, text="Play", command=play)
button_play.pack(side='left')

button_stop = tk.Button(buttons, text="Stop", command=stop, state='disabled')
button_stop.pack(side='left')

# ---- /end buttons ----

window_app.mainloop()

cap.release()