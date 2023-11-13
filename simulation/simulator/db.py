import time
from queue import Empty
import threading

def run_db_simulator(buzzer_queue, pitch, callback, stop_event):
    while not stop_event.is_set():
        try:
            action = buzzer_queue.get(timeout=1)
            if action == "buzz":
                callback('on',0)             
                with threading.Lock():
                    p = "z"
                    if pitch > 500:
                        p = "Z"
                    if pitch > 800:
                        p="Z!"
                    while True:
                        print(p)
                        try:
                            sub_action = buzzer_queue.get(timeout=0.1)
                            print(sub_action)
                            if sub_action == "stop_buzz":
                                break
                            if stop_event.is_set():
                                break
                        except Empty:
                            pass
                        time.sleep(0.1)
                callback('off',0)             
        except Empty:
            pass