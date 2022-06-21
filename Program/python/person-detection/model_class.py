# Model For classification
import yolov5
from numba import jit,cuda

class model_class():
    
    def __init__(self, model_filename, device):
        
        self.device = device
        
        if device == "cuda": # If gpu is available
            self.model = yolov5.YOLOv5(model_filename, device)
        else: # If gpu is NOT available
            self.model = yolov5.load(model_filename, device)
        
    def config_model(self):
        # set model parameters
        # !TODO set parameter value from outside class
        self.model.conf = 0.25  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 10  # maximum number of detections per image
    
    def predict_result(self, img):
        
        if self.device == "cuda":  # if gpu is available
            result = self.model.predict(img)
            predictions = result.pred[0]
        else: #  if gpu is NOT available
            result = self.model(img)
            predictions = result.pred[0]

        return predictions
        

        