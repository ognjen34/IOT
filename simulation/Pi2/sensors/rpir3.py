import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

class RPIR3:
    def __int__(self, pin, name):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.pin = pin
        self.name = name

    def detect_motion(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda x: self.motion_detected_callback())
    
    def motion_detected_callback(self):
        self.mqtt_client.publish("rpir", "detected")

def run_loop(rpir3, callback, stop_event, publish_event, settings):
    rpir3.detect_motion()
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(rpir3.pin)
            GPIO.cleanup()
            break