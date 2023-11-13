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

      

def run_ds_simulator(delay, callback,name, stop_event):
        for _ in generate_values():
            time.sleep(delay) 
            callback(name,0)
            if stop_event.is_set():
                  break
              