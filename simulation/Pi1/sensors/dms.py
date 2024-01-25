import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME


class DMS:

    def __init__(self, settings):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.alarm_on = False
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("ds")
        self.mqtt_client.on_message = lambda client, userdata, message: self.check()
        self.is_typing = False

        self.R1 = settings["R1"]
        self.R2 = settings["R2"]
        self.R3 = settings["R3"]
        self.R4 = settings["R4"]
        self.C1 = settings["C1"]
        self.C2 = settings["C2"]
        self.C3 = settings["C3"]
        self.C4 = settings["C4"]
        self.name = settings['name']
        self.pass_code = []
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)
        GPIO.setup(self.R3, GPIO.OUT)
        GPIO.setup(self.R4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_char(self, line, characters):
        current_key = ""
        GPIO.output(line, GPIO.HIGH)
        if (GPIO.input(self.C1) == 1):
            current_key = characters[0]
        if (GPIO.input(self.C2) == 1):
            current_key = characters[1]
        if (GPIO.input(self.C3) == 1):
            current_key = characters[2]
        if (GPIO.input(self.C4) == 1):
            current_key = characters[3]
        GPIO.output(line, GPIO.LOW)
        if current_key != "":
            print(current_key)
            self.pass_code.append(current_key)
            print(self.pass_code)

    def check(self) :
        if not self.is_typing :
            self.is_typing = True
            if self.alarm_on :
                passcode = None
                while True:
                    passcode = self.get_passcode()
                    if passcode != None:
                        if passcode != ['1','2','3','4'] :
                            self.mqtt_client.publish("alarm","on")
                        else :
                            self.alarm_on = False
                            self.mqtt_client.publish("alarm","off")
                    break
                self.is_typing = False

    def get_passcode(self):
        self.read_char(self.R1, ["1", "2", "3", "A"])
        self.read_char(self.R2, ["4", "5", "6", "B"])
        self.read_char(self.R3, ["7", "8", "9", "C"])
        self.read_char(self.R4, ["*", "0", "#", "D"])
        if len(self.pass_code) == 4:
            pw = self.pass_code
            self.pass_code = []
            return pw
        return None
        


def run_dms_loop(dms, delay, callback, stop_event,publish_event,settings):
    while True:
        passcode = dms.get_passcode()
        if passcode != None:
            if not dms.alarm_on  :
                if passcode == ['1','2','3','4'] :
                    dms.alarm_on = True
            callback(str(passcode),publish_event,settings)
        if stop_event.is_set():
            break
        time.sleep(delay) 