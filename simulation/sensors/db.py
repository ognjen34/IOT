import RPi.GPIO as GPIO
import time
from queue import Empty

class DB(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def buzz(self, pitch, duration):

        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)
           

def run_db_loop(buzzer, pitch, duration, delay, stop_event,queue):
    while True:
        try:
            action = queue.get(timeout=1)
            if action == "buzz":
                buzzer.buzz(pitch, duration)
        except Empty:
            pass
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)