import tkinter as tk
from multiprocessing import Value, Array, Event
import multiprocessing
import ctypes

from project_gui import main as tkinter_window




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
