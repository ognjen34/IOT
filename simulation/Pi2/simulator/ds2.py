import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

def generate_values():
    while True:
        number = random.randint(1, 200)
        time.sleep(2) 
        if number >= 40:
            continue
        print(number)
        yield

      

def run_ds2_simulator(delay, callback,stop_event,publish_event,settings):
        mqtt_client = mqtt.Client()
        mqtt_client.connect(HOSTNAME, 1883, 60)
        for _ in generate_values():
            time.sleep(delay) 
            number = random.randint(3, 7)
            for i in range(number) :
                print("in for",i)
                time.sleep(1)
                if i == 5 :
                    mqtt_client.publish("alarm", "on")
            if number >= 5:       
                mqtt_client.publish("alarm", "off")

                     
            callback(publish_event,settings)
            if stop_event.is_set():
                  break
              