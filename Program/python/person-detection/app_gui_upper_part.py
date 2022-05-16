# app_gui_upper_part
import tkinter as tk

class app_gui_upper_part:

    # GUI upper part -------------------------------   
    def __init__(self, window_app, img1, img2, canvas_w, canvas_h):     

        self.canvas_l_img = img1
        self.canvas_r_img = img2

        self.gui_upper_part = tk.Canvas(
            window_app,
            width = 2*canvas_w,
            height = canvas_h
            )
        self.gui_upper_part.pack(side="top")

        # left display -------------------------------
        self.left_display = tk.Canvas(
            self.gui_upper_part,
            width = canvas_w,
            height = canvas_h
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
            width = canvas_w,
            height = canvas_h
            )
        self.right_display.pack(side='left')
        self.right_display.create_image(
            (canvas_w, 0),
            image=self.canvas_r_img,
            anchor='ne'
            )