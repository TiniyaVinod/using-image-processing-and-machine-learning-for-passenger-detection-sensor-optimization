import numpy as np
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import ttk
from PIL import Image, ImageTk

# --- GUI ---
class app_gui:

    def __init__(self, window_app, img1, img2, width, height):
        
        # Variables
        self.win_app = window_app
        self.canvas_w = width
        self.canvas_h = height
        self.canvas_l_img = img1
        self.canvas_r_img = img2

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
        self.gui_upper_part = tk.Canvas(
            self.win_app,
            width = 2*self.canvas_w,
            height = self.canvas_h
            )
        self.gui_upper_part.pack(side="top")

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

        self.gui_lower_part = tk.Text(
            self.win_app,
            width = (int)(0.25*self.canvas_w),
            height = 10
            )
        self.gui_lower_part.pack()

        #scroll_txt_left = st.ScrolledText(
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
        
        self.tabControl = ttk.Notebook(
            self.gui_lower_part,
            width = self.canvas_w,
            height = self.canvas_h
            )
        self.tabControl.pack(side='right')

        self.tab_camera = ttk.Frame(self.tabControl)
        self.tab_video  = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab_camera, text = 'Camera')
        self.tabControl.add(self.tab_video, text = 'Video')

  # Display text on scroll text widget
    def display_scrolltext(self, txt):
        self.scroll_txt_left.config(state=tk.NORMAL)
        self.scroll_txt_left.insert(tk.END, '\n'+txt)
        #self.scroll_txt_left.see(tk.END)
        self.scroll_txt_left.yview_pickplace("end")
        self.scroll_txt_left.config(state=tk.DISABLED)
        