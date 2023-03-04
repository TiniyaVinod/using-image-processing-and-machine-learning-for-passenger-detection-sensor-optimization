import tkinter as tk
from multiprocessing import Value, Array, Event
import multiprocessing
import ctypes


def update_value(shared_value, shared_value2, label1, label2, window):
    label1.config(text=shared_value.value)
    label2.config(text=shared_value2.value)
    window.after(
        1000, update_value, shared_value, shared_value2, label1, label2, window
    )


def tkinter_window(shared_value, shared_value2):
    window = tk.Tk()
    text = shared_value.value
    frame = tk.Frame(master=window, width=150, height=150)
    frame.pack()

    label1 = tk.Label(master=frame, text=f"{text}", bg="red")
    label1.place(x=0, y=0)

    label2 = tk.Label(master=frame, text=f"{text}", bg="yellow")
    label2.place(x=75, y=75)

    window.after(
        1000, update_value, shared_value, shared_value2, label1, label2, window
    )

    window.mainloop()


def run_counter(shared_value):
    count = 0
    import time

    while True:
        time.sleep(1)
        count += 1
        shared_value.value = count


def run_counter2(shared_value2):
    count = 0
    import time

    while True:
        time.sleep(3)
        count += 3
        shared_value2.value = count


if __name__ == "__main__":

    try:
        multiprocessing.set_start_method("spawn", force=True)
        print("spawned")
    except RuntimeError:
        print("Runtime Error!")
        pass

    context = multiprocessing.get_context("spawn")
    shared_value = context.Value(ctypes.c_int64, 0)
    shared_value2 = context.Value(ctypes.c_int64, 0)

    process1 = multiprocessing.Process(
        target=tkinter_window,
        args=(
            shared_value,
            shared_value2,
        ),
    )
    process2 = multiprocessing.Process(target=run_counter, args=(shared_value,))
    process3 = multiprocessing.Process(target=run_counter2, args=(shared_value2,))
    process1.start()
    process2.start()
    process3.start()
    process1.join()
    process2.join()
    process3.join()


# process1.join()
# process2.join()
