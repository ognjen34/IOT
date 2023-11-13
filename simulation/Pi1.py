
import threading
from settings import load_settings
from components.dht import run_dht
from components.dus import run_dus
from components.dl import run_dl
from components.ds import run_ds
from components.db import run_db


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
        dht1_settings = settings['RDHT1']
        dus1_settings = settings['DUS1']
        dl_settings = settings['DL']
        ds1_settings = settings['DS1']
        db_settings = settings['DB']



        #run_dus(dus1_settings, threads, stop_event)
        run_db(db_settings,threads,stop_event,input_queue)
        #run_ds(dl_settings,"Door button",threads,stop_event)


        input_thread = threading.Thread(target=user_input_thread, args=(input_queue, stop_event,settings))
        input_thread.start()
        threads.append(input_thread)

        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()