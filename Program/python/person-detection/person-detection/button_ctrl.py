from app_gui import app_gui

def play():
    '''
    start stream (run_camera and update_image) 
    and change state of buttons
    '''
    global cap, run_camera

    video_path = gui.getVideoPath()
    
    
    # Check current selected tabb
    select_tab = gui.getSelectedTab()

    if (select_tab == "video"):
        if not exists(video_path):
            txt = "path [ "+video_path+" ] does not exist!"
            gui.display_scrolltext(txt)
            stop()
            return 0
        else:
            cap = cv2.VideoCapture(video_path)   
    else:
        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture("videos/Person_sitandmove.mp4")
        #cap = cv2.VideoCapture(0)

        # Check if source is accessible
        if not cap.isOpened():  
            cap.release()
            stop()
            return 0


    if not run_camera:
        run_camera = True
        
        button_play['state'] = 'disabled'
        button_stop['state'] = 'normal'
        button_pause['state'] = 'normal'
        button_resume['state'] = 'disabled'
        update_frame()
      
def stop():
    '''
    stop stream (run_camera) 
    and change state of buttons
    '''
    global run_camera

    if run_camera:
        run_camera = False

        cap.release()

    button_play['state'] = 'normal'
    button_stop['state'] = 'disabled'
    button_pause['state'] = 'disabled'
    button_resume['state'] = 'disabled'

def pause_frame():
    '''
    pause the stream
    and change state of buttons
    '''
    button_stop['state'] = 'normal'
    button_pause['state'] = 'disabled'
    button_resume['state'] = 'normal'

def resume_frame():
    '''
    resume the stream after pause
    and change state of buttons
    '''
    button_stop['state'] = 'normal'
    button_pause['state'] = 'normal'
    button_resume['state'] = 'diabled'

def click_event(event, x, y):
    
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        gui.display_scrolltext("select position (x,y) :", x,", ", y)