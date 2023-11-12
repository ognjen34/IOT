import time
import random

def generate_values(initial_distance = 15):
      while True:
            distance = initial_distance + random.randint(-10, 10)
            if distance > 10:
                distance = None
            yield distance

      

def run_dus_simulator(delay, callback, stop_event):
        for d in generate_values():
            time.sleep(delay)  
            callback(d, 0)
            if stop_event.is_set():
                  break
              