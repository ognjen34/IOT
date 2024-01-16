import time
from queue import Empty
import threading

def run_db_simulator(queue, pitch, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        try:
            action = queue.get(timeout=1)
            if action == "buzz":
                callback(1,publish_event,settings)             
                with threading.Lock():
                    p = "z"
                    if pitch > 500:
                        p = "Z"
                    if pitch > 800:
                        p="Z!"
                    while True:
                        callback(1,publish_event,settings) 
                        try:
                            sub_action = queue.get(timeout=0.1)
                            print(sub_action)
                            if sub_action == "stop_buzz":
                                break
                            if stop_event.is_set():
                                break
                        except Empty:
                            pass
                        time.sleep(0.5)
                time.sleep(1)
                callback(0,publish_event,settings)             
        except Empty:
            pass