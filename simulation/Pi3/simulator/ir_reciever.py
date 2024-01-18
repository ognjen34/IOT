import time
import random

ButtonsNames = ["LEFT",   "RIGHT",      "UP",       "OFF",       "Cyan",          "Purple",          "Yellow",        "ON",        "4",         "5",         "6",         "7",         "8",          "9",        "*",         "0",        "#"]  # String list in same order as HEX list


def run_ir_receiver_simulator(callback, stop_event, settings, publish_event):
    while True:
        delay = 1
        time.sleep(delay)
        callback(settings['name'], settings, random.choice(ButtonsNames), publish_event)
        if stop_event.is_set():
            break
