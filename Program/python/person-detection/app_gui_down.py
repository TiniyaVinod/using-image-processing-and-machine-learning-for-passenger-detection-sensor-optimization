# app_gui_down
import tkinter as tk
import tkinter.scrolledtext as st

class app_gui_down():


    def __init__(self, window_app, canvas_w, canvas_h):

        self.camera_var = tk.StringVar()
        self.video_var  = tk.StringVar()
        self.record_var = tk.StringVar()
        self.auto_var_1 = tk.StringVar()
        self.auto_var_2 = tk.StringVar()
        self.auto_var_3 = tk.StringVar()
        self.sad_entry  = tk.StringVar()

        self.select_mode = 0 # Mode 0: Camera 1: Video 2: Auto
        self.select_method = 0 # Method 0 : Bg sub 1 : SAD
        self.record_status = 0 # Record Mode only

        default_video_path = "videos/Person_stand.mp4"
        default_bg_path = "images/empty_scene.jpg"
        
        # GUI lower part -------------------------------

        # GUI Scroll text left
        self.scroll_txt_left = st.ScrolledText(
            window_app, 
            width = (int)(0.125*canvas_w),
            height = 20
            )
        self.scroll_txt_left.grid(row=1, column=0)

        # GUI Setting Right
        self.setting_frame = tk.Frame(
            window_app, 
            width = (int)(0.125*canvas_w),
            height = 20)
        self.setting_frame.grid(row=1, column=1)

        i = 0

        tk.Label(
            self.setting_frame,
            text="Control and Setting Panel"
        ).grid(row=i, columnspan=2)

        # Create components with Button, Label and Entry box
        # label
        # label + entry box

        # 1: Camera (DEFAULT)
        self.btn_camera     = tk.Button(self.setting_frame, text="Camera", command=self.press_btn_camera)
        self.btn_camera.grid(row=2*i+1, column=0, sticky='w')
        self.btn_camera.config(relief=tk.SUNKEN)

        self.label_camera   = tk.Label(self.setting_frame, text="Camera Number")
        self.label_camera.grid(row=2*i+2, column=0, sticky='w')

        self.entry_camera   = tk.Entry(self.setting_frame, textvariable=self.camera_var)
        self.entry_camera.grid(row=2*i+2, column=1, sticky='e')       
        i = i + 1

        # 2: Video
        self.btn_video     = tk.Button(self.setting_frame, text="Video", command=self.press_btn_video)
        self.btn_video.grid(row=2*i+1, column=0, sticky='w')

        self.label_video   = tk.Label(self.setting_frame, text="Video Path")
        self.label_video.grid(row=2*i+2, column=0, sticky='w')

        self.entry_video   = tk.Entry(self.setting_frame, textvariable=self.video_var)
        self.entry_video.grid(row=2*i+2, column=1, sticky='e')
        self.entry_video.insert(tk.END, default_video_path)
        i = i + 1

        # 3: Record
        self.btn_record     = tk.Button(self.setting_frame, text="Start Record", command=self.press_btn_start_record)
        self.btn_record.grid(row=2*i+1, column=0, sticky='w')

        self.btn_stop_record = tk.Button(self.setting_frame, text="Stop Record", command=self.press_btn_stop_record)
        self.btn_stop_record.grid(row=2*i+1, column=1, sticky='w')

        self.label_record   = tk.Label(self.setting_frame, text="Export Directory")
        self.label_record.grid(row=2*i+2, column=0, sticky='w')

        self.entry_record   = tk.Entry(self.setting_frame, textvariable=self.record_var)
        self.entry_record.grid(row=2*i+2, column=1, sticky='e')
        self.entry_record.insert(tk.END, "records/record.mp4")
        i = i + 1

        # 4: Auto Mode
        self.btn_auto      = tk.Button(self.setting_frame, text="Auto Mode", command=self.press_btn_auto)
        self.btn_auto.grid(row=2*i+1, column=0, sticky='w')
        
        self.label_auto_1   = tk.Label(self.setting_frame, text="Detect File From")
        self.label_auto_1.grid(row=2*i+2, column=0, sticky='w')

        self.entry_auto_1   = tk.Entry(self.setting_frame, textvariable=self.auto_var_1)
        self.entry_auto_1.grid(row=2*i+2, column=1, sticky='e')

        self.label_auto_2   = tk.Label(self.setting_frame, text="Record Time")
        self.label_auto_2.grid(row=2*i+3, column=0, sticky='w')

        self.entry_auto_2   = tk.Entry(self.setting_frame, textvariable=self.auto_var_2)
        self.entry_auto_2.grid(row=2*i+3, column=1, sticky='e')

        self.label_auto_3   = tk.Label(self.setting_frame, text="Amount of File")
        self.label_auto_3.grid(row=2*i+4, column=0, sticky='w')

        self.entry_auto_3   = tk.Entry(self.setting_frame, textvariable=self.auto_var_3)
        self.entry_auto_3.grid(row=2*i+4, column=1, sticky='e')
        i = i + 1

        i = 5
        # Method Selection -------------------------------------------
        self.label_Method   = tk.Label(self.setting_frame, text="Method Selection")
        self.label_Method.grid(row=2*i+1, column=0, sticky='w')

        # DEFAULT Method, 0: BG Sub , 1: Sum of Abs Diff
        self.btn_bg_sub     = tk.Button(self.setting_frame, text="Background Subtraction", command=self.press_btn_bg_sub)
        self.btn_bg_sub.grid(row=2*i+2, column=0, sticky='w')
        self.btn_bg_sub.config(relief=tk.SUNKEN)

        self.btn_sad        = tk.Button(self.setting_frame, text="Sum of Absolute Differences", command=self.press_btn_sad)
        self.btn_sad.grid(row=2*i+2, column=1, sticky='w')

        self.label_sad_bg_img   = tk.Label(self.setting_frame, text="Background Image Path")
        self.label_sad_bg_img.grid(row=3*i+7, column=0, sticky='w')

        self.entry_sad_bg_img    = tk.Entry(self.setting_frame, textvariable=self.sad_entry)
        self.entry_sad_bg_img.grid(row=3*i+7, column=1, sticky='e')
        self.entry_sad_bg_img.insert(tk.END, default_bg_path)

    # Display text on scroll text widget
    def display_scrolltext(self, txt):
        self.scroll_txt_left.config(state=tk.NORMAL)
        self.scroll_txt_left.insert(tk.END, '\n'+txt)
        self.scroll_txt_left.yview_pickplace("end")
        self.scroll_txt_left.config(state=tk.DISABLED)

    # Button actions for MODE selection
    def press_btn_camera(self):
        self.btn_camera.config(relief=tk.SUNKEN)
        self.btn_video.config(relief=tk.RAISED)
        self.btn_record.config(relief=tk.RAISED)
        self.btn_auto.config(relief=tk.RAISED)

        self.select_mode = 0

    def press_btn_video(self):
        self.btn_camera.config(relief=tk.RAISED)
        self.btn_video.config(relief=tk.SUNKEN)
        self.btn_record.config(relief=tk.RAISED)
        self.btn_auto.config(relief=tk.RAISED)

        self.select_mode = 1
        self.record_status = 0

    def press_btn_start_record(self):
        self.btn_camera.config(relief=tk.SUNKEN)
        self.btn_video.config(relief=tk.RAISED)
        self.btn_record.config(relief=tk.SUNKEN)
        self.btn_auto.config(relief=tk.RAISED)

        self.record_status = 1

    def press_btn_stop_record(self):

        self.record_status = 0
        return 0
        
        
    def press_btn_auto(self):
        self.btn_camera.config(relief=tk.RAISED)
        self.btn_video.config(relief=tk.RAISED)
        self.btn_record.config(relief=tk.RAISED)
        self.btn_auto.config(relief=tk.SUNKEN)

        self.select_mode = 3
        self.record_status = 0

    # Button actions for METHOD selection
    def press_btn_bg_sub(self):
        self.btn_bg_sub.config(relief=tk.SUNKEN)
        self.btn_sad.config(relief=tk.RAISED)

        self.select_method = 0

    def press_btn_sad(self):
        self.btn_bg_sub.config(relief=tk.RAISED)
        self.btn_sad.config(relief=tk.SUNKEN)

        self.select_method = 1


    # Method for get value from entry boxes
    def get_camera_number(self):
        return self.entry_camera.get()

    def get_video_path(self):
        return self.entry_video.get() 

    def get_record_export_path(self):
        return self.record_var.get()

    def get_auto_dir(self):
        var_auto = [self.auto_var_1, self.auto_var_2, self.auto_var_3]
        return var_auto

    def get_select_mode(self):
        return self.select_mode

    def get_select_method(self):
        return self.select_method

    def get_bg_img_path(self):
        return self.sad_entry.get()

    def get_record_status(self):
        return self.record_status
