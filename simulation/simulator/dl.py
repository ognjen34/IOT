
from queue import Empty
import time


def run_dl_simulator(input_queue, delay, callback, stop_event):
    while not stop_event.is_set():
        try:
            action = input_queue.get(timeout=1)
            if action == "on":
                callback("ON")
            elif action == "off":
                callback("OFF")
        except Empty:
            pass
        time.sleep(delay)