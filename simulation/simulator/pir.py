import random 
import time

def generate_values():
    while True:
        time.sleep(5)
        value = random.randint(0, 1)
        yield value
    
def run_pir_simulator(delay, callback, stop_event, name):
    for value in generate_values():
        if value == 0:
            callback(name)
        if stop_event.is_set():
            break