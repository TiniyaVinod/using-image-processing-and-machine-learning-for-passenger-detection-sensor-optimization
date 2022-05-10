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
        radio_btn_camera['state'] = 'disabled'
        radio_btn_video['state'] = 'disabled'

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
        radio_btn_camera['state'] = 'normal'
        radio_btn_video['state'] = 'normal'
        

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

# Display text on text widget
def display_text(txt):
    textwidget_left.config(state=tk.NORMAL)
    textwidget_left.insert(tk.END, '\n'+txt)
    textwidget_left.config(state=tk.DISABLED)

def update_frame():

    ret, frame = cap.read()

     # If can't read frame
    if (ret is None) | (ret == False):
        display_text("Can't read from camera.")
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
        bgSubFrame = backSub.apply(frame)
        img2 = Image.fromarray(bgSubFrame)
        photo_img2.paste(img2)
        

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

cap = cv2.VideoCapture("videos/Person_stand.mp4")
#cap = cv2.VideoCapture(0)
# Check if source is accessible
if not cap.isOpened():  
    display_text("Can't turn on camera")
    cap.release()
    exit(1)

backSub = cv2.createBackgroundSubtractorKNN()

# first frame with clear white image
canvas_w = 640
canvas_h = 640

white_img = np.zeros([canvas_w, canvas_h, 3], dtype=np.uint8)
white_img.fill(255) 

# create app window
window_app = tk.Tk()
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


textwidget = tk.Text(
    window_app, 
    width = (int)(0.25*canvas_w),
    height = 10
    )
textwidget.pack()

textwidget_left = tk.Text(
    textwidget, 
    width = (int)(0.125*canvas_w),
    height = 10
    )
textwidget_left.pack(side='left')

textwidget_right = tk.Text(
    textwidget, 
    width = (int)(0.125*canvas_w),
    height = 10
    )
textwidget_right.pack(side='right')


# --- main ---

source_sel =tk.IntVar()

# ---- Radio buttons ----
radio_buttons = tk.Frame(window_app)
radio_buttons.pack()

radio_btn_camera = tk.Radiobutton(radio_buttons, text="Camera", var = source_sel, value=0)
radio_btn_camera.pack(side='left')

radio_btn_video = tk.Radiobutton(radio_buttons, text="Video", var = source_sel, value=1)
radio_btn_video.pack(side='left')


# ---- buttons ----
buttons = tk.Frame(window_app)
buttons.pack(side='bottom', fill='x')

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