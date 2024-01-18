
from queue import Empty
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

def run_dl_simulator(callback, stop_event, publish_event, settings):
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe("dpir1")
    mqtt_client.on_message = lambda client, userdata, message: dl_on(callback, publish_event, settings, message)
    while not stop_event.is_set():
        pass


def dl_on(callback,publish_event,settings,message) :
    payload = message.payload.decode("utf-8")
    callback(1,publish_event,settings)
    print("on")
    time.sleep(10)
    callback(0,publish_event,settings)
    print("off")




