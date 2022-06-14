# Model For classification
import yolov5
from numba import jit, cuda

class model_class():
    
    def __init__(self, model_filename):
        self.model = yolov5.load(model_filename)
        
    def config_model(self):
        # set model parameters
        # !TODO set parameter value from outside class
        self.model.conf = 0.25  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 10  # maximum number of detections per image
        
    @jit
    def predict_result(self, img):
        
        result = self.model(img)
        predictions = result.pred[0]
        
        return predictions
        

        