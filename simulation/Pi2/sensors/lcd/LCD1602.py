#!/usr/bin/env python3

from .PCF8574 import PCF8574_GPIO
from .Adafruit_LCD1602 import Adafruit_CharLCD
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME
from time import sleep, strftime
from datetime import datetime
class LCD(object) :

    def __init__(self) :
        PCF8574_address = 0x27  
        PCF8574A_address = 0x3F  
        self.mcp = None
        try:
            self.mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)
        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=self.mcp)
        self.mcp.output(3,1)     
        self.lcd.begin(16,2)  
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(HOSTNAME, 1883, 60)
        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("gdht/temperature")
        self.mqtt_client.subscribe("gdht/humidity")     
        self.humidity = "0"
        self.temperature = "0" 
   
        
    def display(self):
            self.lcd.setCursor(0,0)  
            self.lcd.message( 'Temperature: ' + self.temperature+'\n' )
            self.lcd.message( 'Humidity: ' + self.humidity+'\n' )

            sleep(1)
    def on_msg(self,message):
        payload = message.payload.decode("utf-8")
        if message.topic == "gdht/temperature" :
            self.temperature = payload
        if message.topic == "gdht/humidity" :
            self.humidity = payload
         
            
    def destroy(self):
        self.lcd.clear()
        
    


def run_lcd_loop(lcd,text, delay,stop_event):
    lcd.mqtt_client.on_message = lambda client, userdata, message: lcd.on_msg(message)
    while True:
        lcd.display()
        if stop_event.is_set():
                lcd.destroy()
                break
        sleep(delay)


