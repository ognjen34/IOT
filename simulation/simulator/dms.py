import time
import random
import threading

keyboard_inputs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D']

def generate_values(delay):
    while(True):
        time.sleep(delay)
        input = random.randint(0, len(keyboard_inputs)-1)
        keyboard_input = keyboard_inputs[input]
        yield keyboard_input

def run_dms_simualtor(delay, callback, stop_event,publish_event,settings):
    for keyboard_input in generate_values(delay):
        with threading.Lock():
            callback(keyboard_input,publish_event,settings)
        if stop_event.is_set():
                break