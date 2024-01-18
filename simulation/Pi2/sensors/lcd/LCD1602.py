#!/usr/bin/env python3

from .PCF8574 import PCF8574_GPIO
from .Adafruit_LCD1602 import Adafruit_CharLCD

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
        
   
        
    def display(self,text):
            self.lcd.setCursor(0,0)  
            self.lcd.message( 'Text: ' + text+'\n' )
            self.lcd.message( 'Text2: ' + "loool:D"+'\n' )

            sleep(1)
            
    def destroy(self):
        self.lcd.clear()
        
    


def run_lcd_loop(lcd,text, delay,stop_event):
    while True:
        lcd.display(text)
        if stop_event.is_set():
                lcd.destroy()
                break
        sleep(delay)


