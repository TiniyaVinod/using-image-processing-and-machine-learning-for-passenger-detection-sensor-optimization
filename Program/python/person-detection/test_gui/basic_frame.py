import tkinter as tk

window = tk.Tk()

window.minsize(750, 750)
window.maxsize(750, 750)

frame_top_left = tk.Frame(
    master=window, borderwidth=1, background="red", height=10, width=20
)
frame_top_left.grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
)

label_tl = tk.Label(master=frame_top_left, height=19, width=38)
label_tl.pack()

frame_top_right = tk.Frame(master=window, borderwidth=1, background="yellow")
frame_top_right.grid(row=0, column=1, padx=5, pady=5)

label_tr = tk.Label(master=frame_top_right, height=19, width=38)
label_tr.pack()

frame_middle_left = tk.Frame(master=window, borderwidth=1, background="yellow")
frame_middle_left.grid(row=1, column=0, padx=5, pady=5)

label_ml = tk.Label(master=frame_middle_left, height=4, width=38)
label_ml.pack()

frame_middle_right = tk.Frame(master=window, borderwidth=1, background="red")
frame_middle_right.grid(row=1, column=1, padx=5, pady=5)

lable_mr = tk.Label(master=frame_middle_right, height=4, width=38)
lable_mr.pack()


frame_bottom_left = tk.Frame(master=window, borderwidth=1, background="red")
frame_bottom_left.grid(row=2, padx=5, pady=5)

label_bl = tk.Label(master=frame_bottom_left, height=15, width=80)
label_bl.pack()


frame_lowest_level = tk.Frame(master=window, borderwidth=1, background="yellow")
frame_lowest_level.grid(row=3)

label_ll = tk.Label(master=frame_lowest_level, height=4, width=80)
label_ll.pack()

window.mainloop()
