import cv2
import numpy as np

img1 = cv2.imread('images/frames/frame0.jpg')
img2 = cv2.imread('images/frames/frame230.jpg')

img1 = cv2.resize(img1, (0, 0), None, .25, .25)
img2 = cv2.resize(img2, (0, 0), None, .25, .25)

img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

img_diff = cv2.absdiff(img1, img2)

numpy_horizontal  = np.hstack((img1, img2, img_diff))
numpy_horizontal_concat = np.concatenate((img1, img2, img_diff), axis=1)

cv2.imshow('Numpy Horizontal Concat', numpy_horizontal_concat)
cv2.waitKey(0)