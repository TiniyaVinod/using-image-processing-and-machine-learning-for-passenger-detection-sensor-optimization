import tkinter as tk
from PIL import ImageTk, Image


def main(shared_value=None, shared_value2=None):
    window = tk.Tk()
    window.minsize(750, 750)
    window.maxsize(750, 750)

    # top frame

    top_frame = tk.Frame(master=window, borderwidth=1, height=50, width=100)
    top_frame.grid(row=0, column=0, padx=5, pady=5)

    top_frame_top_left = tk.Frame(master=top_frame, borderwidth=1)
    top_frame_top_left.grid(
        row=0,
        column=0,
    )
    image = Image.open("bishal.jpg")

    resized_photo = ImageTk.PhotoImage(image.resize((320, 320)), Image.ANTIALIAS)

    label_tl = tk.Label(
        master=top_frame_top_left,
        # height=19,
        # width=38,
        background="red",
        image=resized_photo,
        borderwidth=3,
    )
    label_tl.pack()

    top_frame_top_right = tk.Frame(master=top_frame, borderwidth=1)
    top_frame_top_right.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)

    label_tr = tk.Label(
        master=top_frame_top_right, height=19, width=38, background="yellow"
    )
    label_tr.pack()

    top_frame_bottom_left = tk.Frame(master=top_frame, borderwidth=1)
    top_frame_bottom_left.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        ipadx=5,
        ipady=5,
    )

    top_label__bl = tk.Label(
        master=top_frame_bottom_left, height=4, width=38, background="red"
    )
    top_label__bl.pack()

    if shared_value:
        text_to_show = shared_value.value
    else:
        text_to_show = "Prediction Result"

    top_label__bl.config(text=text_to_show)

    top_frame_bottom_right = tk.Frame(master=top_frame, borderwidth=1)
    top_frame_bottom_right.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5)

    top_label__br = tk.Label(
        master=top_frame_bottom_right, height=4, width=38, background="yellow"
    )
    top_label__br.pack()

    if shared_value2:
        text_to_show2 = shared_value2.value
    else:
        text_to_show2 = "Camera at : Localhost//"
    top_label__br.config(text=text_to_show2)

    # bottom frame

    bottom_frame = tk.Frame(master=window, borderwidth=1, height=30, width=79)
    bottom_frame.grid(row=1, column=0)

    bottom_frame_top_part = tk.Frame(master=bottom_frame, borderwidth=1)
    bottom_frame_top_part.grid(
        row=0,
        column=0,
    )
    bottom_frame_label_top_part = tk.Label(
        master=bottom_frame_top_part, height=13, width=79, background="green"
    )
    bottom_frame_label_top_part.pack()

    bottom_frame_bottom_part = tk.Frame(master=bottom_frame, borderwidth=1)
    bottom_frame_bottom_part.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
    bottom_frame_label_bottom_part = tk.Label(
        master=bottom_frame_bottom_part, height=4, width=79, background="yellow"
    )
    bottom_frame_label_bottom_part.pack()

    update_value(top_label__bl, top_label__br, shared_value, shared_value2, window)

    window.mainloop()


def update_value(label1, label2, shared_value, shared_value2, window):
    label1.config(text=shared_value.value)
    label2.config(text=shared_value2.value)
    window.after(
        1000, update_value, label1, label2, shared_value, shared_value2, window
    )


if __name__ == "__main__":
    main()
