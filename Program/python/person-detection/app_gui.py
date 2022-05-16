import numpy as np
import tkinter as tk
from tkinter import ttk
from app_gui_upper_part import app_gui_upper_part
from app_gui_lower_part import app_gui_lower_part

# --- GUI ---
class app_gui():

    def __init__(self, window_app, img1, img2, width, height):
        
        # Variables
        #self.winapp = window_app
        self.canvas_w = width
        self.canvas_h = height
        
        

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
        self.gui_upper_part = app_gui_upper_part(window_app, img1, img2, width, height)
        
        self.gui_lower_part = app_gui_lower_part(window_app, width, height)
        
        # Tab 1: Camera
        #self.tab_camera = ttk.Frame(self.tab_control, name="camera")
#
        #self.tab_control.add(self.tab_camera, text = 'Camera')
        #self.tab_control.tab(1, text='camera')
#
        ## Tab 2: Auto Record
        #self.tab_camera = ttk.Frame(self.tab_control, name="auto_record")
        #self.tab_control.add(self.tab_camera, text = 'Auto Record')
        #self.tab_control.tab(2, text='auto_record')
#
        ## Tab 3: Extract Frames
        #self.tab_extract_frame = ttk.Frame(self.tab_control, name="extract_frames")
        #self.tab_control.add(self.tab_extract_frame, text = 'Extract_Frames')
        #self.tab_control.tab(3, text='extract_frames')
#
        #self.extract_frame_label = ttk.Label(
        #    self.tab_extract_frame, 
        #    text ="Video Path: "
        #    ).grid(
        #        row = 0,
        #        column = 0               
        #        )
        #        
        #self.extract_frame_entrybox = tk.Entry(
        #    self.tab_extract_frame,
        #    width=(int)(0.2*self.canvas_w),
        #    textvariable=self.video_path
        #    ).grid(
        #        row = 0,
        #        column = 1
        #        )

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

    
