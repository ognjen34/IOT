import time
import random

def generate_values():
    while True:
        number = random.randint(1, 200)
        time.sleep(2) 
        if number >= 40:
            continue
        print(number)
        yield

      

def run_ds2_simulator(delay, callback,stop_event,publish_event,settings):
        for _ in generate_values():
            time.sleep(delay) 
            callback(publish_event,settings)
            if stop_event.is_set():
                  break
              