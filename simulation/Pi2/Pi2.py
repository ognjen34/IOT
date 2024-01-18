
import threading
import sys
sys.path.append('../')
from settings import load_settings
from components.gsg import run_gsg
from components.lcd import run_lcd
from components.ds2 import run_ds2
from components.dus2 import run_dus2
from components.dpir2 import run_dpir2
from components.gdht import run_gdht
from components.rpir3 import run_rpir3
from components.rdht3 import run_rdht3




import time
from queue import Queue


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def user_input_thread(queue, stop_event,settings):
    while True:
        try:
            user_action = input()
            if user_action.upper() == settings["DL"]["on_key"]:
                queue.put("on")
            if user_action.upper() == settings["DL"]["off_key"]:
                queue.put("off")
            if user_action.upper() == settings["DB"]["on_key"]:
                queue.put("buzz")
            if user_action.upper() == settings["DB"]["off_key"]:
                queue.put("stop_buzz")
        except:
            time.sleep(0.001)
            if stop_event.is_set():
                break


if __name__ == "__main__":
    input_queue = Queue()
    print('Pi1 is starting')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        #gsg_settings = settings['GSG']
        #lcd_settings = settings['GLCD']
        #ds2_settings = settings['DS2']
        dus2_settings = settings['DUS2']
        dpir2_settings = settings['DPIR2']
        #gdht_settings = settings['GDHT']
        #rpir3_settings = settings['RPIR3']
        #rdht3_settings = settings['RDHT3']

        #run_gsg(gsg_settings, threads, stop_event)
        #run_lcd(lcd_settings, threads, stop_event)
        #run_ds2(ds2_settings,threads,stop_event)
        #run_rpir3(rpir3_settings, threads, stop_event)

        run_dus2(dus2_settings, threads, stop_event)
        run_dpir2(dpir2_settings, threads, stop_event)
        #run_gdht(gdht_settings, threads, stop_event)
        #run_rdht3(rdht3_settings, threads, stop_event)


        input_thread = threading.Thread(target=user_input_thread, args=(input_queue, stop_event,settings))
        input_thread.start()
        threads.append(input_thread)

        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()