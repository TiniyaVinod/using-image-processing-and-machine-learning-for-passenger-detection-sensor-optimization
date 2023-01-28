import time
import multiprocessing
from multiprocessing import Value, Array, Event
from datetime import datetime


event_p1_for_sync = Event()
event_p2_for_sync = Event()


shared_timestamp = Value("i", 0)


def start_process():
    process1 = multiprocessing.Process(
        target=slower_func,
        args=(
            event_p1_for_sync,
            event_p2_for_sync,
            shared_timestamp,
        ),
    )
    process2 = multiprocessing.Process(
        target=faster_func,
        args=(
            event_p1_for_sync,
            event_p2_for_sync,
            shared_timestamp,
        ),
    )

    process3 = multiprocessing.Process(
        target=timestamp_updater, args=(shared_timestamp,)
    )
    process1.start()
    process2.start()
    process3.start()


def slower_func(event_p1_for_sync, event_p2_for_sync, shared_timestamp):
    print("Inside slower function")
    run_loop_conditional = True
    while run_loop_conditional:
        print()
        print()
        print(
            f"-----------------Inside while loop of slower func-----{shared_timestamp.value}----------"
        )
        print()
        print()
        time.sleep(1)
        event_p1_for_sync.set()
        if event_p2_for_sync.wait(8):
            event_p2_for_sync.clear()
            run_loop_conditional = True
        else:
            run_loop_conditional = False


def faster_func(event_p1_for_sync, event_p2_for_sync, shared_timestamp):
    print("Inside faster function")
    run_loop_conditional = True
    while run_loop_conditional:
        print()
        print()
        print(
            f"++++++++++Inside while loop of faster func+++++++++ {shared_timestamp.value}+++++++"
        )
        print()
        print()
        time.sleep(7)
        event_p2_for_sync.set()
        if event_p1_for_sync.wait(8):
            event_p1_for_sync.clear()
            run_loop_conditional = True
        else:
            run_loop_conditional = False


def timestamp_updater(shared_timestamp):
    while True:
        timestamp = (
            datetime.today() - datetime.today().replace(hour=0, minute=0, second=0)
        ).seconds
        shared_timestamp.value = timestamp


start_process()
