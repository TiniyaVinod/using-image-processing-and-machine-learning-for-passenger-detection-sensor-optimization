import yolov5
import cv2 
import numpy as np

# load pretrained model
model = yolov5.load('yolov5s.pt')

# or load custom model
#model = yolov5.load('train/best.pt')c
  
# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image

#img = cv2.imread('images/frames/frame1.jpg') # Test Empty
img = cv2.imread('images/frames/frame230.jpg') # Test Person

# perform inference
results = model(img)

# inference with larger input size
#results = model(img, size=1280)

# inference with test time augmentation
#results = model(img, augment=True)

# parse results
predictions = results.pred[0]
boxes = predictions[:, :4] # x1, y1, x2, y2
scores = predictions[:, 4]
categories = predictions[:, 5]

# show detection bounding boxes on image
print(results.print())


#img_output = cv2.drawKeypoints(img, boxes, np.array([]), (0,0,255))

cv2.rectangle(img, (boxes[0,0],boxes[0,1]), (boxes[0,2],boxes[0,3]), (0,255,0), (10))

cv2.imshow("", img)
cv2.waitKey(0)