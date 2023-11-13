
import threading
from settings import load_settings
from components.dht import run_dht
from components.dus import run_dus
from components.dl import run_dl
from components.pir import run_pir
from components.dms import run_dms



import time
from queue import Queue


try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def user_input_thread(led_queue, stop_event,settings):
    while True:
        try:
            user_action = input()
            if user_action.upper() == settings["DL"]["on_key"]:
                led_queue.put("on")
            elif user_action.upper() == settings["DL"]["off_key"]:
                led_queue.put("off")
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
        dpir1_settings = settings['DPIR1']
        dms_settings = settings['DMS']

        #run_dus(dus1_settings, threads, stop_event)
        #run_dl(dl_settings,threads,stop_event,input_queue)
        #run_pir(dpir1_settings, threads, stop_event, "DPIR1")
        run_dms(dms_settings, threads, stop_event, 'DMS')

        #input_thread = threading.Thread(target=user_input_thread, args=(input_queue, stop_event,settings))
        #input_thread.start()
        #threads.append(input_thread)

        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()