#!/usr/bin/env python3

import tkinter
import cv2
import numpy as np
import PIL.Image, PIL.ImageTk
import time
from LiveVideoCapture import LiveVideoCapture
from detect_main import FaceDetection

class App:
    def __init__(self, window, window_title, face_cascade, video_source=0):
        # main window for camera
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        # store face cascade model
        self.face_cascade = face_cascade
        
        # open video source (by default this will try to open the computer webcam)
        self.vid = LiveVideoCapture(self.window, self.video_source)

        # initialise face detection object
        self.face_detect = FaceDetection(self.face_cascade)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot_face)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)


        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot_face(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
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
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.window.after(self.delay, self.update)
       

# declare face cascade model 
haar_face_cascade = cv2.CascadeClassifier('mdls/haarcascade_frontalface_default.xml')

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Face-Recogniser", face_cascade=haar_face_cascade)