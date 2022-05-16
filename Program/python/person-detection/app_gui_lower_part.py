# app_gui_lower_part
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import ttk
from app_gui_tab_video import app_gui_tab_video

class app_gui_lower_part():
#    pass

    def __init__(self, window_app, canvas_w, canvas_h):

        # GUI lower part -------------------------------
        self.gui_lower_part = tk.Text(
            window_app,
            width = (int)(0.25*canvas_w),
            height = 10
            )
        self.gui_lower_part.pack()

        # GUI Scroll text left
        self.scroll_txt_left = st.ScrolledText(
            self.gui_lower_part, 
            width = (int)(0.125*canvas_w),
            height = 20
            )
        self.scroll_txt_left.pack(side='left')

        self.scroll_txt_left.config(
            self.gui_lower_part, 
            width = (int)(0.125*canvas_w),
            height = 20
        )
        
        # GUI tab Control right
        self.tab_control = ttk.Notebook(
            self.gui_lower_part,
            width = canvas_w,
            height = canvas_h,
            name="tab_master"
            )
        self.tab_control.pack(side='right')

        self.tab_video = app_gui_tab_video(self.tab_control, canvas_w, canvas_h)

    # Display text on scroll text widget
    def display_scrolltext(self, txt):
        self.scroll_txt_left.config(state=tk.NORMAL)
        self.scroll_txt_left.insert(tk.END, '\n'+txt)
        self.scroll_txt_left.yview_pickplace("end")
        self.scroll_txt_left.config(state=tk.DISABLED)
        
    def getSelectedTab(self):
        select_tab = self.tab_control.tab(self.tab_control.select(), "text") 
        return select_tab

