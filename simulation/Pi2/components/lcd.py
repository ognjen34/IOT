

from simulator.lcd import run_lcd_simulator
import threading
import time
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json





def lcd_callback(text, gsg_settings, code="LCD_OK"):

    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"LCD DISPLAYED: {text}")

    


def run_lcd(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting lcd sumilator")
            lcd_thread = threading.Thread(target = run_lcd_simulator, args=(10,"pisa", lcd_callback, stop_event,settings))
            lcd_thread.start()
            threads.append(lcd_thread)
            print("lcd sumilator started")
        else:
            from sensors.lcd.LCD1602 import run_lcd_loop, LCD
            print("Starting lcd loop")
            lcd = LCD()
            lcd_thread = threading.Thread(target=run_lcd_loop, args=(lcd,"pisa", 2, stop_event))
            lcd_thread.start()
            threads.append(lcd_thread)
            print("lcd loop started")
