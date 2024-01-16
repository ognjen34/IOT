import time
import random


def run_lcd_simulator(delay,text, callback, stop_event, settings):
    while True:
        time.sleep(delay)
        callback(text, settings)
        if stop_event.is_set():
            break
