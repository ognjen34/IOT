import RPi.GPIO as GPIO
import time
from queue import Empty
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

class BB(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("alarm")
        self.is_buzzing = False

    def alarm(self,callback, publish_event, settings, message):
        payload = message.payload.decode("utf-8")
        
        if payload == 'on' :
            self.is_buzzing = True
            callback(1,publish_event,settings)             

        if payload == 'off' :
            self.is_buzzing = False
            callback(0,publish_event,settings)             


    def buzz(self, pitch, duration):
        period = 1.0 / pitch
        delay = period / 2
        try:
            while True:
                if self.is_buzzing :
                    GPIO.output(self.pin, True)
                    time.sleep(delay)
                    GPIO.output(self.pin, False)
                    time.sleep(delay)
        except KeyboardInterrupt:
            GPIO.output(self.pin, False)

def run_bb_loop(buzzer, pitch, duration, delay,callback, stop_event,queue,publish_event, settings):
    buzzer.mqtt_client.on_message = lambda client, userdata, message: buzzer.alarm(callback, publish_event, settings, message)
    buzzer.buzz(pitch, duration)

    while True:
        if stop_event.is_set():
            GPIO.cleanup()
            break
