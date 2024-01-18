import random 
import time

def generate_values(delay):
    while True:
        time.sleep(delay)
        value = random.randint(0, 1)
        yield value
    
def run_dpir1_simulator(delay, callback, stop_event, publish_event, settings):
    for value in generate_values(delay):
        if value == 0:
            callback( publish_event, settings)
        if stop_event.is_set():
            break