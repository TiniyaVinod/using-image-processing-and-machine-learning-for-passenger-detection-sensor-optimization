# Model For classification
import yolov5
import math

class model_class():
    
    def __init__(self, config):
        
        self.device = config["computing_device"]
        model_filename = config["model_filename"]
        
        if self.device == "cuda": # If gpu is available
            self.model = yolov5.YOLOv5(model_filename, self.device)
        else: # If gpu is NOT available
            self.model = yolov5.load(model_filename)
            
        self.default_config(config)
        
    def default_config(self, config):
        # set default value to parameters
        self.model.conf = config["model_confidence_threshold"]  # NMS confidence threshold
        self.model.iou = config["model_iou_threshold"]  # NMS IoU threshold
        self.model.agnostic = bool(config["model_agnostic"])  # NMS class-agnostic
        self.model.multi_label = bool(config["model_multi_label"])  # NMS multiple labels per box
        self.model.max_det = config["model_max_detection"]  # maximum number of detections per image

    # Change parameter by selection
    # Set NMS confidence threshold
    def conf_threshold(self, conf_num):
        self.model.conf = conf_num
    
    # Set NMS IoU threshold
    def iou_threshold(self, iou_num):
        self.model.iou = iou_num
        
    # Set Maximum Detection
    def max_detection(self, det_num):
        self.model.max_det = det_num
    
    # Predict result
    def predict_result(self, img):
        
        if self.device == "cuda":  # if gpu is available
            result = self.model.predict(img)
            predictions = result.pred[0]
        else: #  if gpu is NOT available
            result = self.model(img)
            print("Total Result")
            print("--------------++++++++++++++++++-----------------")
            # print(f"Result Pandas: {result.pandas().xyxy[0]}\n")
            # print(f"Result Pandas confidence zero: {result.pandas().xyxy[0].confidence[0]}\n")
            # print(f"Result Pandas name zero: {result.pandas().xyxy[0].name[0]}\n")
            output_result_text = []
            for i in range(len(result.pandas().xyxy[0].confidence)):
                output_result_text.append(f"Class: {(result.pandas().xyxy[0].name[i]).upper()}, Confidence : {math.floor(result.pandas().xyxy[0].confidence[i]*100)} %")
            # result.print()
            # print("Result Pred : ", result.pred, "\n")
            print(output_result_text)
            if len(output_result_text)==0:
                output_result_text.append("NO DETECTION!")
            print("-------------------------------")
            predictions = result.pred[0]
            # print("predictions :", predictions)

        return (predictions, output_result_text)
        

        