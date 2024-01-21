import time
import random
import threading
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

keyboard_inputs = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D']
keyboard_password = ['1','2','3','4']
class DMS(object) :
    def __init__(self) :
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.alarm_on = False
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("ds")

    def generate_values(self,delay):
        is_password = False
        while(True):
            is_password = False
            if random.randint(0,1) == 1 :
                is_password = True
            if is_password :
                time.sleep(delay)
                yield keyboard_password
            else :
                time.sleep(delay)
                keyboard_input = []
                for i in range(4):
                    rnum = random.randint(0, len(keyboard_inputs)-1)
                    keyboard_input.append(keyboard_inputs[rnum])
                yield keyboard_input
    def generate_value(self,delay = 2):
        is_password = False
        if random.randint(0,1) == 1 :
            is_password = True
        if is_password :
            time.sleep(delay)
            return keyboard_password
        else :
            time.sleep(delay)
            keyboard_input = []
            for i in range(4):
                rnum = random.randint(0, len(keyboard_inputs)-1)
                keyboard_input.append(keyboard_inputs[rnum])
            return keyboard_input

    def check(self) :
        if self.alarm_on :
            pin = self.generate_value()
            print("bla",pin)

            if pin != keyboard_password :
                self.mqtt_client.publish("alarm","on")
            else :
                self.alarm_on = False
                self.mqtt_client.publish("alarm","off")


def run_dms_simualtor(delay, callback, stop_event,publish_event,settings):
    dms = DMS()
    dms.mqtt_client.on_message = lambda client, userdata, message: dms.check()

    for keyboard_input in dms.generate_values(60):
        with threading.Lock():

            if not dms.alarm_on :
                print(keyboard_input)
                callback(str(keyboard_input),publish_event,settings)

                if keyboard_input == keyboard_password :
                    time.sleep(10)
                    print("Alarm is on")
                    dms.alarm_on = True

            if dms.alarm_on :
                 pass
            if stop_event.is_set():
                break