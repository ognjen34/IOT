import time
from queue import Empty
import threading
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME



class BB(object) :
    def __init__(self,callback, publish_event, settings) :
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("alarm")
        self.mqtt_client.subscribe("buzz")

        self.mqtt_client.on_message = lambda client, userdata, message: self.alarm(callback, publish_event, settings, message)
        self.is_buzzing = False

    def alarm(self,callback, publish_event, settings, message):
        payload = message.payload.decode("utf-8")
        
        if payload == 'on' :
            self.is_buzzing = True
            callback(1,publish_event,settings)             

        if payload == 'off' :
            self.is_buzzing = False
            callback(0,publish_event,settings)             





def run_bb_simulator(queue, pitch, callback, stop_event, publish_event, settings):
    bb = BB(callback, publish_event, settings)
    while not stop_event.is_set():
        if bb.is_buzzing :
            print("buzz")
            callback(1,publish_event,settings)             
            time.sleep(3)
        