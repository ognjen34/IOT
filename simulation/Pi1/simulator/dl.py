
from queue import Empty
import time


def run_dl_simulator(input_queue, delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        try:
            action = input_queue.get(timeout=1)
            if action == "on":
                callback(1,publish_event,settings)
            elif action == "off":
                callback(0,publish_event,settings)
        except Empty:
            pass
        time.sleep(delay)