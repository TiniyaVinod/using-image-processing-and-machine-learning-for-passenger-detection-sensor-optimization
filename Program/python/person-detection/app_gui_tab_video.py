#api_gui_tab_video
import tkinter as tk
from tkinter import ttk 

class app_gui_tab_video():

    def __init__(self, tab_master,canvas_w, canvas_h):

        self.video_path = tk.StringVar()
        self.bg_img_path = tk.StringVar()
        self.blob_min = tk.StringVar()
        self.blob_max = tk.StringVar()
            
        # Tab 0: Video 
        self.tab_video  = ttk.Frame(tab_master, name="video")
        tab_master.add(self.tab_video, text = 'video')
        tab_master.tab(0, text='video')
        
        self.videoPath_label = ttk.Label(
            self.tab_video, 
            text ="Video Path: "
            ).grid(
                row = 0,
                column = 0               
                )
                
        self.videoPath_entrybox = tk.Entry(
            self.tab_video,
            width=(int)(0.2*canvas_w),
            textvariable=self.video_path
            ).grid(
                row = 0,
                column = 1
                )

        self.bgPath_label = ttk.Label(
            self.tab_video, 
            text ="BG Image Path: "
            ).grid(
                row = 2,
                column = 0               
                )

        self.bgPath_entrybox = tk.Entry(
            self.tab_video,
            width=(int)(0.2*canvas_w),
            textvariable=self.bg_img_path
            ).grid(
                row = 2,
                column = 1
                )

        self.blob_label = ttk.Label(
            self.tab_video,
            text="Blob Indicator Setting"
        ).grid(
            row = 3,
            column = 0
            )

        self.blob_min_area_label = ttk.Label(
            self.tab_video,
            text="Blob Min Area : "
        ).grid(
            row = 4,
            column = 0,
            sticky='w'
            )

        self.bgPath_entrybox = tk.Entry(
            self.tab_video,
            width=(int)(0.05*canvas_w),
            textvariable=self.blob_min
            ).grid(
                row = 4,
                column = 1,
                sticky='w'
                )   

        self.blob_max_area_label = ttk.Label(
            self.tab_video,
            text="Blob Max Area : "
        ).grid(
            row = 5,
            column = 0,
            sticky='w'
            )

        self.blob_max_area_entrybox = tk.Entry(
            self.tab_video,
            width=(int)(0.05*canvas_w),
            textvariable=self.blob_max
            ).grid(
                row = 5,
                column = 1,
                sticky='w'
                )  

    def get_VideoPath(self):
        return "videos/Person_stand.mp4"# TODO del this line and uncomment the following
        #return self.video_path.get()

    def get_BGImagePath(self):
        return "images/empty_scene.jpg"# TODO del this line and uncomment the following
        #return self.bg_img_path.get()
   
    def get_blob_min(self):

        try:
            int(self.blob_min.get())
            return int(self.blob_min.get())
        except ValueError:
            self.display_scrolltext("Blob min input must be a number")

    def get_blob_max(self):

        try:
            int(self.blob_max.get())
            return int(self.blob_max.get())
        except ValueError:
            self.display_scrolltext("Blob max input must be a number")
