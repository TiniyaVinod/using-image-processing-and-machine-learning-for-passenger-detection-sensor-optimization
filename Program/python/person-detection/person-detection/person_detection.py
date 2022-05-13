#!/usr/bin/env python3

from msilib.schema import RadioButton
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime

def play():
    '''
    start stream (run_camera and update_image) 
    and change state of buttons
    '''
    global run_camera

    if not run_camera:
        run_camera = True
        
        button_play['state'] = 'disabled'
        button_stop['state'] = 'normal'
        #button_bgSub['state'] = 'normal'
        button_ROI['state'] = 'disabled'
        update_frame()
      


def stop():
    '''
    stop stream (run_camera) 
    and change state of buttons
    '''
    global run_camera

    if run_camera:
        run_camera = False

        button_play['state'] = 'normal'
        button_stop['state'] = 'disabled'
        #button_bgSub['state'] = 'disabled'
        button_ROI['state'] = 'normal'

def createROI():

    '''
    draw ROI into frame and filter out non-ROI area with black
    '''
    
    global ROI_Flag

    if not ROI_Flag:
        ROI_Flag = True
        button_ROI['state'] = 'disabled'
        
        cv2.setMouseCallback(canvas_left, click_event)

    else:
        ROI_Flag = False
        button_ROI['state'] = 'normal'
        
        return frame

def click_event(event, x, y):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        display_text("select position (x,y) :", x,", ", y)
    
        
# Display text on text widget
def display_text(txt):
    scroll_txt_left.config(state=tk.NORMAL)
    scroll_txt_left.insert(tk.END, '\n'+txt)
    scroll_txt_left.see(tk.END)
    scroll_txt_left.config(state=tk.DISABLED)

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

    global frame

    ret, frame = cap.read()

     # If can't read frame
    if (ret is None) | (ret == False):
        cap.release()

    # Resize frame
    dim = (canvas_w, canvas_h)
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    # correct the color
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # mirror horizontally
    frame = np.fliplr(frame)
    
    img = Image.fromarray(frame)
    photo_img.paste(img)

    # background subtraction
    bgSubFrame = backSub.apply(frame)
    #denoise_img = cv2.fastNlMeansDenoising(bgSubFrame,3,7,21) # cost a lot of delay

    # blob detection
    blob_keypoints = blob_detector.detect(bgSubFrame)
    if len(blob_keypoints) == 0:
        img2 = Image.fromarray(bgSubFrame)
        text = dateTimeObj.strftime("%m/%d/%Y, %H:%M:%S")+': Empty Scene'
        display_text(text)
    else:
        img_with_keypoints = cv2.drawKeypoints(
            bgSubFrame,
            blob_keypoints,
            np.array([]),
            (0,0,255),
            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        img2 = Image.fromarray(img_with_keypoints)
        text = dateTimeObj.strftime("%m/%d/%Y, %H:%M:%S")+' Human'
        display_text(text)
    
    #img2 = Image.fromarray(bgSubFrame)
    photo_img2.paste(img2)
    

    if run_camera:
        window_app.after(10, update_frame)

# --- main ---

run_camera = False
bgSubFlag = False
ROI_Flag = False

backSub = cv2.createBackgroundSubtractorKNN()

blob_detector = init_blob_detector()

dateTimeObj = datetime.now()

# first frame with clear white image
canvas_w = 320
canvas_h = 320

white_img = np.zeros([canvas_w, canvas_h, 3], dtype=np.uint8)
white_img.fill(255) 

# create app window
window_app = tk.Tk()
window_app.title("Person Detection")
window_app.geometry = ("1080x400")
#window_app.resizable(width=True, height=True)

image = Image.fromarray(white_img)
photo_img = ImageTk.PhotoImage(image)
photo_img2 = ImageTk.PhotoImage(image)

# --- GUI ---
# Create a canvas that can fit the video size
canvas = tk.Canvas(
    window_app,
    width = 2*canvas_w,
    height = canvas_h
    )
canvas.pack(side="top")

canvas_left = tk.Canvas(
    canvas,
    width = canvas_w,
    height = canvas_h
    )
canvas_left.pack(side='left')
canvas_left.create_image((0,0), image=photo_img, anchor='nw')

canvas_right = tk.Canvas(
    canvas,
    width = canvas_w,
    height = canvas_h
    )
canvas_right.pack(side='left')
canvas_right.create_image((0,0), image=photo_img2, anchor='nw')

lower_widget = tk.Text(
    window_app, 
    width = (int)(0.25*canvas_w),
    height = 10
    )
lower_widget.pack()

scroll_txt_left = st.ScrolledText(
    lower_widget, 
    width = (int)(0.125*canvas_w),
    height = 20
    )
scroll_txt_left.pack(side='left')

tabControl = ttk.Notebook(
    lower_widget, 
    width = canvas_w,
    height = canvas_h
    )
tabControl.pack(side='right')

tab_camera = ttk.Frame(tabControl)
tab_video  = ttk.Frame(tabControl)

tabControl.add(tab_camera, text = 'Camera')
tabControl.add(tab_video, text = 'Video')



# --- main ---

source_sel = tk.IntVar()

#cap = cv2.VideoCapture("videos/Person_stand.mp4")
#cap = cv2.VideoCapture("videos/Empty_scene+chair_2.mp4")
cap = cv2.VideoCapture("videos/Person_sitandmove.mp4")
#cap = cv2.VideoCapture(0)
# Check if source is accessible
if not cap.isOpened():  
    display_text("Source is invalid")
    cap.release()
    stop()
    exit(1)


# ---- buttons ----
buttons = tk.Frame(window_app)
buttons.pack(side='bottom', fill='x')

button_play = tk.Button(buttons, text="Play", command=play)
button_play.pack(side='left')

button_stop = tk.Button(buttons, text="Stop", command=stop, state='disabled')
button_stop.pack(side='left')

#button_bgSub = tk.Button(buttons, text="BG subtraction", command=bgSubtraction, state='disabled')
#button_bgSub.pack(side='left')

button_ROI = tk.Button(buttons, text="Select ROI", command=createROI, state='disabled')
button_ROI.pack(side='left')

# ---- /end buttons ----

window_app.mainloop()

cap.release()