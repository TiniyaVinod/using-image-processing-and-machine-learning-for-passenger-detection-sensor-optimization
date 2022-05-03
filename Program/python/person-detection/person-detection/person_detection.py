
#!/usr/bin/env python3

import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from LiveVideoCapture import LiveVideoCapture
from detect_main import FaceDetection

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

# Toggle background subtraction
def bgSubtraction():

    '''
    apply background subtraction
    '''

    global bgSubFlag

    if not bgSubFlag:
        bgSubFlag = True
    else:
        bgSubFlag = False

def drawROI():


    # !TODO : create another popup window and select ROI from there
    # then return coordinate and make a filter out of it
    roi = cv2.selectROI(canvas)


def update_frame():

    ret, frame = cap.read()
    
    # correct the color
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # mirror horizontally
    frame = np.fliplr(frame)
    img = Image.fromarray(frame)

    if bgSubFlag == True:
        fgMask = backSub.apply(frame)
        img = Image.fromarray(fgMask)

    photo_img.paste(img)

    window_app.after(10, update_frame)

# --- main ---

run_camera = False
bgSubFlag = False

backSub = cv2.createBackgroundSubtractorKNN()

# Video Source Object
cap = cv2.VideoCapture(1)

# first frame
ret, frame = cap.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = np.fliplr(frame)

# create app window
window_app = tk.Tk()
window_app.geometry = ("880x800")
window_app.resizable(width=True, height=True)

image = Image.fromarray(frame)
photo_img = ImageTk.PhotoImage(image)

# declare face cascade model
haar_face_cascade = cv2.CascadeClassifier('mdls/haarcascade_frontalface_default.xml')

# Create a canvas that can fit the above video source size
canvas = tk.Canvas(
    window_app,
    width = 880,
    height = 640
    ) # 640x840
canvas.pack(fill='both', expand=True)

canvas.create_image((0,0), image=photo_img, anchor='nw')

# -- buttons
buttons = tk.Frame(window_app)
buttons.pack(fill='x')

button_play = tk.Button(buttons, text="Play", command=play)
button_play.pack(side='left')

button_stop = tk.Button(buttons, text="Stop", command=stop, state='disabled')
button_stop.pack(side='left')

button_filter = tk.Button(buttons, text="BG subtraction", command=bgSubtraction)
button_filter.pack(side='left')

button_filter = tk.Button(buttons, text="Select ROI", command=drawROI)
button_filter.pack(side='left')

# -- /end buttons

window_app.mainloop()

cap.release()