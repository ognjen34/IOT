import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

def run_lcd_simulator(delay,text, callback, stop_event, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe("gdht/temperature")
    mqtt_client.subscribe("gdht/humidity")

    mqtt_client.on_message = lambda client, userdata, message: print_data(callback, settings, message)
    
    while True:
        if stop_event.is_set():
            break
def print_data(callback, settings, message):
    text = ""
    payload = message.payload.decode("utf-8")

    if message.topic == "gdht/temperature" :
        text = f"Temperature: {payload}"
    if message.topic == "gdht/humidity" :
        text = f"Humidity: {payload}"
    callback(text, settings)



