
#!/usr/bin/env python3

import tkinter as tk
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk
import time
from LiveVideoCapture import LiveVideoCapture
from detect_main import FaceDetection

class main_program:
    def __init__(self, window, window_title, face_cascade, video_source=0):
        
        # main window for application
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # store face cascade model
        self.face_cascade = face_cascade

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(
            window,
            width = 840,
            height = 640
            ) # 640x840
        self.canvas.grid(row = 0, column = 0)

        # Button snapshot
        self.btn_onoff = tk.Button(
            window,
            text = "Turn on/off Camera",
            width = 20,
            height = 5,
            command = self.toggle_camera
            )
        self.btn_onoff.grid(row = 1, column = 0)

        # After it is called once, the update method will be automatically called every delay 15 milliseconds
        self.delay = 15
        
        self.update()

        self.window.mainloop()
    
    def toggle_camera(self):
        # Toggle on/off Camera
        self.camera_enable_flag == True

        
    def snapshot_face(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):

        # open video source (by default this will try to open the computer webcam)
        self.vid = LiveVideoCapture(self.window, self.video_source)
            
        # initialise face detection object
        self.face_detect = FaceDetection(self.face_cascade)

        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        # detect face in frame
        face_coordinate = self.face_detect.detect_face(frame)
        if len(face_coordinate) != 0:
            (x, y, w ,h) = face_coordinate[0] # store only one set of face coordinate
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        if ret:
            # swap horizontally
            frame = np.fliplr(frame)
            # put image 
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(440, 340, image = self.photo)

        self.window.after(self.delay, self.update)

# declare face cascade model
haar_face_cascade = cv2.CascadeClassifier('mdls/haarcascade_frontalface_default.xml')

# Create a window and pass it to the Application object
program_window = tk.Tk()
program_window.geometry("880x800")
program_window.resizable(width=True, height=True)
main_program(program_window, "Face-Detector", face_cascade=haar_face_cascade)