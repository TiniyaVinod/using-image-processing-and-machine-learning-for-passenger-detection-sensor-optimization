import numpy as np
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import Variable, ttk
from PIL import Image, ImageTk

# --- GUI ---
class app_gui:

    def __init__(self, window_app, img1, img2, width, height):
        
        # Variables
        #self.winapp = window_app
        self.canvas_w = width
        self.canvas_h = height
        self.canvas_l_img = img1
        self.canvas_r_img = img2
        self.video_path = tk.StringVar()
        self.bg_img_path = tk.StringVar()
        self.select_method = tk.StringVar()

        # Gui Components
        # ------------------------------------
        # |                |                 |
        # |             Gui upper part       |
        # |                |                 |
        # | left_display   | right_display   |
        # ------------------------------------
        # |                |                 |
        # |             Gui lower part       |
        # |                |                 |
        # | scroll_txt_left| tab_control     |
        # ------------------------------------
        
        # Create a canvas that can fit the video size
        
        # GUI upper part -------------------------------        
        self.gui_upper_part = tk.Canvas(
            window_app,
            width = 2*self.canvas_w,
            height = self.canvas_h
            )
        self.gui_upper_part.pack(side="top")

        # left display -------------------------------
        self.left_display = tk.Canvas(
            self.gui_upper_part,
            width = self.canvas_w,
            height = self.canvas_h
            )
        self.left_display.pack(side='left')
        self.left_display.create_image(
            (0, 0),
            image=self.canvas_l_img,
            anchor='nw'
            )

        # right display -------------------------------
        self.right_display = tk.Canvas(
            self.gui_upper_part,
            width = self.canvas_w,
            height = self.canvas_h
            )
        self.right_display.pack(side='left')
        self.right_display.create_image(
            (self.canvas_w, 0),
            image=self.canvas_r_img,
            anchor='ne'
            )

        # GUI lower part -------------------------------
        self.gui_lower_part = tk.Text(
            window_app,
            width = (int)(0.25*self.canvas_w),
            height = 10
            )
        self.gui_lower_part.pack()

        # GUI Scroll text left
        self.scroll_txt_left = st.ScrolledText(
            self.gui_lower_part, 
            width = (int)(0.125*self.canvas_w),
            height = 20
            )
        self.scroll_txt_left.pack(side='left')

        self.scroll_txt_left.config(
            self.gui_lower_part, 
            width = (int)(0.125*self.canvas_w),
            height = 20
        )
        
        # GUI tab Control right
        self.tab_control = ttk.Notebook(
            self.gui_lower_part,
            width = self.canvas_w,
            height = self.canvas_h,
            name="tab_master"
            )
        self.tab_control.pack(side='right')

         # Tab 0: Video 
        self.tab_video  = ttk.Frame(self.tab_control, name="video")
        self.tab_control.add(self.tab_video, text = 'video')
        self.tab_control.tab(0, text='video')
        
        self.videoPath_label = ttk.Label(
            self.tab_video, 
            text ="Video Path: "
            ).grid(
                row = 0,
                column = 0               
                )
                
        self.videoPath_entrybox = tk.Entry(
            self.tab_video,
            width=(int)(0.2*self.canvas_w),
            textvariable=self.video_path
            ).grid(
                row = 0,
                column = 1
                )

        #self.button_bg_sub = tk.Button(
        #    self.tab_video,
        #    text="BG Sub",          
        #    ).grid(
        #        row = 1,
        #        column = 0
        #        )

        #self.button_sad = tk.Button(
        #    self.tab_video,
        #    text="SAD",
        #    ).grid(
        #        row = 1,
        #        column = 1
        #        )

        self.bgPath_label = ttk.Label(
            self.tab_video, 
            text ="BG Image Path: "
            ).grid(
                row = 2,
                column = 0               
                )

        self.bgPath_entrybox = tk.Entry(
            self.tab_video,
            width=(int)(0.2*self.canvas_w),
            textvariable=self.bg_img_path
            ).grid(
                row = 2,
                column = 1
                )

        # Tab 1: Camera
        self.tab_camera = ttk.Frame(self.tab_control, name="camera")

        self.tab_control.add(self.tab_camera, text = 'Camera')
        self.tab_control.tab(1, text='camera')

        # Tab 2: Auto Record
        self.tab_camera = ttk.Frame(self.tab_control, name="auto_record")
        self.tab_control.add(self.tab_camera, text = 'Auto Record')
        self.tab_control.tab(2, text='auto_record')

        # Tab 3: Extract Frames
        self.tab_extract_frame = ttk.Frame(self.tab_control, name="extract_frames")
        self.tab_control.add(self.tab_extract_frame, text = 'Extract_Frames')
        self.tab_control.tab(3, text='extract_frames')

        self.extract_frame_label = ttk.Label(
            self.tab_extract_frame, 
            text ="Video Path: "
            ).grid(
                row = 0,
                column = 0               
                )
                
        self.extract_frame_entrybox = tk.Entry(
            self.tab_extract_frame,
            width=(int)(0.2*self.canvas_w),
            textvariable=self.video_path
            ).grid(
                row = 0,
                column = 1
                )

        # ---- Buttons ----
        #buttons = tk.Frame(window_app)
        #buttons.pack(side='bottom', fill='x')

        #button_play = tk.Button(buttons, text="Play", command=play)
        #button_play.pack(side='left')

        #button_stop = tk.Button(buttons, text="Stop", command=stop, state='disabled')
        #button_stop.pack(side='left')

        #button_pause = tk.Button(buttons, text="Pause", command=pause_frame, state='disabled')
        #button_pause.pack(side='left')

        #button_resume = tk.Button(buttons, text="Resume", command=resume_frame, state='disabled')
        #button_resume.pack(side='left')

        # ---- /end buttons ----

    # Display text on scroll text widget
    def display_scrolltext(self, txt):
        self.scroll_txt_left.config(state=tk.NORMAL)
        self.scroll_txt_left.insert(tk.END, '\n'+txt)
        self.scroll_txt_left.yview_pickplace("end")
        self.scroll_txt_left.config(state=tk.DISABLED)
        
    def getSelectedTab(self):
        select_tab = self.tab_control.tab(self.tab_control.select(), "text") 
        return select_tab

    def getVideoPath(self):
        return "videos/Person_stand.mp4"# TODO del this line and uncomment the following
        #return self.video_path.get()

    def getBGImagePath(self):
        return "images/empty_scene.jpg"# TODO del this line and uncomment the following
        return self.bg_img_path.get()
   