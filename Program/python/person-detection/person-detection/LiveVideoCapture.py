import cv2

class LiveVideoCapture:
    def __init__(self, window, video_source=0):
        # Open the video src
        self.vid = cv2.VideoCapture(video_source)
            
        # Get video src width and height
        self.width  = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Get window
        self.window = window
            
        #if not self.vid.isOpened():
        #   raise ValueError("Unable to open video source", video_source)

    # Release the video src when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.mainloop()

    def get_frame(self):
        ret, frame = self.vid.read()

        if self.vid.isOpened():
            # ret, frame = self.vid.read()

            if ret:
                # Return a boolean success flag and the current frame converted to RGB
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)                  