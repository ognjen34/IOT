import RPi.GPIO as GPIO
import time
from queue import Empty
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

class DL(object):
    def __init__(self, pin) -> None:
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("dpir1")

    def turn_on_10(self,callback, publish_event, settings, message):
        GPIO.output(self.pin, GPIO.HIGH)
        callback(1,publish_event,settings)
        time.sleep(10)
        GPIO.output(self.pin, GPIO.LOW)
        callback(0,publish_event,settings)



    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

def run_dl_loop(input_queue, dl, delay, callback, stop_event,publish_event, settings):
    dl.mqtt_client.on_message = lambda client, userdata, message: dl.turn_on_10(callback, publish_event, settings, message)

    while True:
        if stop_event.is_set():
            GPIO.cleanup()
            break

        time.sleep(delay)