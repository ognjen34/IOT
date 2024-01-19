import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME

class Brgb(object):
    def __init__(self, settings, callback):
        self.callback = callback
        GPIO.setmode(GPIO.BCM)
        self.RED_PIN= settings['red_pin']
        self.GREEN_PIN = settings['green_pin']
        self.BLUE_PIN = settings['blue_pin']
        
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("brgb")
        
    def run(self):
        self.mqtt_client.on_message = lambda client, userdata, message: self.set_mode(message)
              
    def set_mode(self, message):
        mode = message.payload.decode("utf-8")
        if mode == "OFF":
            self.turnOff()
        if mode == "RED":
            self.red()
        if mode == "BLUE":
            self.blue()
        if mode == "GREEN":
            self.green()
        if mode == "WHITE":
            self.white()
        if mode == "YELLOW":
            self.yellow()
        if mode == "PURPLE":
            self.purple()
        if mode == "LIGHTBLUE":
            self.lightBlue()
        self.callback(self.settings, mode)
        
    def turnOff(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
    
    def white(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def red(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)

    def green(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
        
    def blue(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def yellow(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
        
    def purple(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def lightBlue(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
