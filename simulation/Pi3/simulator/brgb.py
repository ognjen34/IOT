import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

def run_brgb_simulator(settings, callback, stop_event):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe("brgb")
    mqtt_client.on_message = lambda client, userdata, message: set_mode(message, settings, callback)
     
def set_mode(message, settings, callback):
    mode = message.payload.decode("utf-8")
    callback(settings, mode)
    