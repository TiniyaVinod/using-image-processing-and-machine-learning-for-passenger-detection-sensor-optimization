import cv2
import numpy as np

class FaceDetection:
    def __init__(self, face_cascade):
        self.face_cascade = face_cascade

    # Detect face from frame and return face if found
    def detect_face(self, colored_img, scaleFactor = 1.1):
        img_copy = colored_img.copy()
        
        # convert to grayscale
        gray_img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        face_coordinate = self.face_cascade.detectMultiScale(gray_img, scaleFactor=scaleFactor, minNeighbors=5)
        
        return face_coordinate

        # crop face from frame
        # for (x, y, w ,h) in face:
        # if len(face_coordinate) != 0:
        #    return face_coordinate
        # else:
        #    return None
            # (x, y, w ,h) = face_coordinate[0] # store only one set of face coordinate
            # cv2.rectangle(img_copy, (x,y), (x+w, y+h), (0, 255, 0), 2)
            
    def detect_eyes(eye_cascade, colored_img, scaleFactor = 1.1):
        img_copy = colored_img.copy()

        # convert to grayscale
        gray_img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        eyes = eye_cascade.detectMultiScale(gray_img, scaleFactor=scaleFactor) 

        for (x, y, w ,h) in eyes:
            cv2.rectangle(img_copy, (x,y), (x+w, y+h), (0, 255, 0), 2)
        
        return eyes   