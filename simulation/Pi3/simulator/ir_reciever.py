import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

ButtonsNames = ["LEFT",   "RIGHT",      "UP",       "OFF",       "RED",          "GREEN",          "BLUE",        "ON",        "4",         "5",         "6",         "7",         "8",          "9",        "*",         "0",        "#"]  # String list in same order as HEX list


def run_ir_receiver_simulator(callback, stop_event, settings, publish_event):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    while True:
        delay = 3
        time.sleep(delay)
        mode = random.choice(ButtonsNames)
        mqtt_client.publish("brgb", mode)
        callback(settings['name'], settings, mode, publish_event)
        if stop_event.is_set():
            break
