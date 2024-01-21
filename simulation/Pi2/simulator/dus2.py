import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME


class DUS2(object):
    def __init__(self,callback, publish_event, settings) :
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("dpir2")
        self.mqtt_client.on_message = lambda client, userdata, message: self.detected(callback, publish_event, settings, message)
        self.people_inside = 0
    def generate_values(self,initial_distance = 15):
            distance = initial_distance + random.randint(-10, 10)
            return distance
    def detected(self,callback,publish_event,settings,message) :
        detect1= self.generate_values()
        callback(detect1,publish_event,settings)
        time.sleep(3)
        detect2= self.generate_values()
        callback(detect2,publish_event,settings)

        if detect2 == detect1 :
            detect2= self.generate_values()

        if detect1 > detect2 :
            self.mqtt_client.publish("people", +1)
        else :
            self.mqtt_client.publish("people", -1)

        print(self.people_inside)



def run_dus2_simulator(callback, stop_event,publish_event,settings):
        dus2 = DUS2(callback, publish_event, settings)
        while True : 
            if stop_event.is_set():
                  break
            

