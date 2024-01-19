import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

class DUS2(object):
    def __innit__(self, TRIG_PIN, ECHO_PIN):
        self.TRIG_PIN = TRIG_PIN
        self.ECHO_PIN = ECHO_PIN
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("dpir2")
        self.people_inside = 0
    
    def get_distance(self):
        GPIO.output(self.TRIG_PIN, False)
        time.sleep(0.2)
        GPIO.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(self.ECHO_PIN) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.ECHO_PIN) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300)/2
        return distance
    
    def detected(self,callback,publish_event,settings,message) :
        detect1= self.get_distance()
        callback(detect1,publish_event,settings)
        time.sleep(3)
        detect2= self.get_distance()
        callback(detect2,publish_event,settings)

        if detect2 == detect1 :
            detect2= self.generate_values()

        if detect1 > detect2 :
            self.mqtt_client.publish("people", +1)
        else :
            self.mqtt_client.publish("people", -1)

        print(self.people_inside)


def run_dus2_loop(dus2, callback, stop_event,publish_event,settings):
    dus2.mqtt_client.on_message = lambda client, userdata, message: dus2.detected(callback, publish_event, settings, message)
    while True:
        if stop_event.is_set():
                break
