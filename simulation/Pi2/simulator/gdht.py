import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

def generate_values(initial_temp = 25, initial_humidity=20):
      temperature = initial_temp
      humidity = initial_humidity
      while True:
            temperature = temperature + random.randint(-1, 1)
            humidity = humidity + random.randint(-1, 1)
            if humidity < 0:
                  humidity = 0
            if humidity > 100:
                  humidity = 100
            yield humidity, temperature

      

def run_gdht_simulator(delay, callback, stop_event, publish_event, settings):
        mqtt_client = mqtt.Client()
        mqtt_client.connect(HOSTNAME, 1883, 60)
        for h, t in generate_values():
            time.sleep(delay) 
            callback(h, t, publish_event, settings)
            mqtt_client.publish("gdht/temperature", t)
            mqtt_client.publish("gdht/humidity", h)
            if stop_event.is_set():
                  break
              