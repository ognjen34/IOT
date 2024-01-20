import random 
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME


def generate_values(delay):
    while True:
        time.sleep(delay)
        value = random.randint(0, 1)
        yield value
    
def run_rpir4_simulator(delay, callback, stop_event, publish_event, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    for value in generate_values(delay):
        if value == 0:
            callback( publish_event, settings)
            mqtt_client.publish("rpir", "detected")
            time.sleep(10)

        if stop_event.is_set():
            break