
import threading
import sys
sys.path.append('../')
from settings import load_settings
from components.dus import run_dus
from components.dl import run_dl
from components.ds import run_ds
from components.db import run_db
from components.dpir1 import run_dpir1
from components.rpir1 import run_rpir1
from components.rpir2 import run_rpir2
from components.rdht1 import run_rdht1
from components.rdht2 import run_rdht2



from components.dms import run_dms



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
        #rdht1_settings = settings['RDHT1']
        #rdht2_settings = settings['RDHT2']

        #dus1_settings = settings['DUS1']
        #dl_settings = settings['DL']
        #ds_settings = settings['DS1']
        ds1_settings = settings['DS1']
        db_settings = settings['DB']
        #dpir1_settings = settings['DPIR1']
        #rpir1_settings = settings['RPIR1']
        #rpir2_settings = settings['RPIR2']
        dms_settings = settings['DMS']


        #run_dus(dus1_settings, threads, stop_event)
        
        run_db(db_settings,threads,stop_event,input_queue)
        run_ds(ds1_settings,threads,stop_event)
        #run_rdht1(rdht1_settings, threads, stop_event)
        #run_rdht2(rdht2_settings, threads, stop_event)


        

        #run_dus(dus1_settings, threads, stop_event)
        #run_dl(dl_settings,threads,stop_event,input_queue)
        #run_dpir1(dpir1_settings, threads, stop_event)
        #run_rpir1(rpir1_settings, threads, stop_event)
        #run_rpir2(rpir2_settings, threads, stop_event)
        run_dms(dms_settings, threads, stop_event)

        input_thread = threading.Thread(target=user_input_thread, args=(input_queue, stop_event,settings))
        input_thread.start()
        threads.append(input_thread)

        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()