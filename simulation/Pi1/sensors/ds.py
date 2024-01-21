import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

class DS(object):
    def __init__(self, pin) -> None:
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.start_time = None
    
    def press(self):
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.button_changed, bouncetime=100)
    
    def release(self):
        GPIO.remove_event_detect(self.pin)
        self.start_time = None
        self.mqtt_client.publish("alarm", "off")
    
    def button_changed(self, event):
        if GPIO.input(self.pin) == GPIO.HIGH:
            # Button released
            self.release()
        else:
            # Button pressed
            self.start_time = time.time()


def run_ds_loop(ds, delay, callback, stop_event, publish_event, settings):
    while True:
        ds.press()
        if ds.start_time is not None:
            elapsed_time = time.time() - ds.start_time
            if elapsed_time >= 5:
                ds.mqtt_client.publish("alarm", "on")

        callback(publish_event, settings)
        if stop_event.is_set():
            ds.release()  # Ensure that the release method is called before breaking the loop
            break
        time.sleep(delay)
