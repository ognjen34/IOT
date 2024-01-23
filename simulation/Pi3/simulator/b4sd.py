import time 
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

received_message = None

def run_b4sd_simulator(settings, stop_event, callback, publish_event):
        mqtt_client = mqtt.Client()
        mqtt_client.connect(HOSTNAME, 1883, 60)
        mqtt_client.subscribe("b4sd")
        mqtt_client.loop_start()
        global received_message
        mqtt_client.on_message = lambda client, userdata, message: get_message(message)
        alarm = ""
        while True:       
            pass
            print(received_message)
            if received_message != None:
                alarm = received_message.payload.decode('utf-8')
                print(alarm)
            if stop_event.is_set():
                break
            n = time.ctime()[11:13] + time.ctime()[14:16]
            s = str(n).rjust(4)
            print(alarm)
            if str(s) == alarm:
                print("ALARM")
                mqtt_client.publish("buzz", "on")
                mqtt_client.publish("alarmClock", "on")
                alarm = ""
                received_message = None
            if alarm == "alarmClockOff":
                print("NIJE VISE ALARM")
                mqtt_client.publish("buzz", "off")
                mqtt_client.publish("alarmClock", "off")
                alarm = ""
                received_message = None

            callback(settings, s, publish_event)
            time.sleep(5)


def get_message(message):
    print(message.payload.decode('utf-8'))
    global received_message
    received_message = message
    
