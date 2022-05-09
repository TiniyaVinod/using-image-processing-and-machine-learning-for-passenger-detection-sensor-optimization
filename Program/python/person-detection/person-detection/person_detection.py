#!/usr/bin/env python3

import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk

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
        button_bgSub['state'] = 'normal'
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
        button_bgSub['state'] = 'disabled'
        button_ROI['state'] = 'normal'
        

# Toggle background subtraction
def bgSubtraction():

    '''
    apply background subtraction
    '''

    global bgSubFlag

    if not bgSubFlag:
        bgSubFlag = True
        button_bgSub['state'] = 'disabled'
    else:
        bgSubFlag = False
        button_bgSub['state'] = 'normal'

def createROI(frame):

    '''
    draw ROI into frame and filter out non-ROI area with black
    '''
    
    global ROI_Flag

    if not ROI_Flag:
        ROI_Flag = True
        button_ROI['state'] = 'disabled'

        roi = cv2.selectROI(frame)

        pos_x = int(roi[1])
        len_x = int(roi[1] + roi[3])

        pos_y = int(roi[0])
        len_y = int(roi[0] + roi[2])
        frame[pos_x:len_x, pos_y:len_y, :] = 0
        return frame

    else:
        ROI_Flag = False
        button_ROI['state'] = 'normal'
        
        return frame

def update_frame():

    #global frame

    ret, frame = cap.read()
    
    # If can't read frame
    if ret is None:
        print("Can't read from camera")
        cap.release()
        exit(1)

    # Resize frame
    dim = (canvas_w, canvas_h)
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    # correct the color
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # mirror horizontally
    frame = np.fliplr(frame)
    
    # background subtraction
    if bgSubFlag == True:
        frame = backSub.apply(frame)

    # ROI Selection
    if ROI_Flag == True:
        frame = createROI(frame)

    img = Image.fromarray(frame)
    photo_img.paste(img)

    if run_camera:
        window_app.after(10, update_frame)

# --- main ---

run_camera = False
bgSubFlag = False
ROI_Flag = False

backSub = cv2.createBackgroundSubtractorKNN()

# Video Source Object
cap = cv2.VideoCapture("videos/person_stand.mp4")
#cap = cv2.VideoCapture(0)

# Check if source is accessible
if not cap.isOpened():
    print("Can't open camera")
    cap.release()
    exit(1)

# first frame with clear white image
canvas_w = 640
canvas_h = 480

white_img = np.zeros([canvas_h, canvas_w, 3], dtype=np.uint8)
white_img.fill(255) 

# create app window
window_app = tk.Tk()
#window_app.geometry = ("880x800")
window_app.resizable(width=True, height=True)

image = Image.fromarray(white_img)
photo_img = ImageTk.PhotoImage(image)

# --- GUI ---

# Create a canvas that can fit the above video source size
canvas = tk.Canvas(
    window_app,
    width = canvas_w,
    height = canvas_h
    ) # 640x480
canvas.pack(fill='both', expand=True)

canvas.create_image((0,0), image=photo_img, anchor='nw')

textwidget = tk.Text(window_app, height = 10, width = 80)

canvas.size()
textwidget.pack()


# ---- buttons ----
buttons = tk.Frame(window_app)
buttons.pack(fill='x')

button_play = tk.Button(buttons, text="Play", command=play)
button_play.pack(side='left')

button_stop = tk.Button(buttons, text="Stop", command=stop, state='disabled')
button_stop.pack(side='left')

button_bgSub = tk.Button(buttons, text="BG subtraction", command=bgSubtraction, state='disabled')
button_bgSub.pack(side='left')

button_ROI = tk.Button(buttons, text="Select ROI", command=createROI, state='disabled')
button_ROI.pack(side='left')

# ---- /end buttons ----

window_app.mainloop()

cap.release()