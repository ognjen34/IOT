import RPi.GPIO as GPIO
import time


class DS(object):
    def __init__(self, pin) -> None:
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    def press(self):
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback =
        self.button_pressed, bouncetime = 100)
            

    def button_pressed(self,event):
        print("BUTTON PRESS DETECTED")
        


def run_ds_loop(ds,delay, callback, stop_event,publish_event,settings):
		while True:
			ds.press()
			callback(publish_event,settings)
			if stop_event.is_set():
					break
			time.sleep(delay)  
