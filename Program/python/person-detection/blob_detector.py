import cv2

def init_blob_detector():
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 1
    params.maxThreshold = 255
    params.filterByArea = True
    params.minArea = 4000
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
