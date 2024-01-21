import time 
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

received_message = None

def run_b4sd_simulator(settings, stop_event, callback, publish_event):
        mqtt_client = mqtt.Client()
        mqtt_client.connect(HOSTNAME, 1883, 60)
        mqtt_client.loop_start()
        mqtt_client.subscribe("b4sd")

        global received_message
        alarm = ""
        while True:
            mqtt_client.on_message = lambda client, userdata, message: get_message(message)
            if received_message != None:
                alarm = received_message.payload.decode('utf-8')
                print(alarm)
            if stop_event.is_set():
                break
            n = time.ctime()[11:13] + time.ctime()[14:16]
            s = str(n).rjust(4)
            if str(s) == alarm:
                print("ALARM")
                mqtt_client.publish("buzz", "on")
            if alarm == "":
                mqtt_client.publish("buzz", "off")

            callback(settings, s, publish_event)
            time.sleep(5)

def get_message(message):
    global received_message
    received_message = message