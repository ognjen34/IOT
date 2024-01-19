
import threading
import sys
sys.path.append('../')
from settings import load_settings



import time
from queue import Queue
from components.b4sd import run_b4sd
from components.ir_receiver import run_ir_receiver
from components.brgb import run_brgb
from components.rpir4 import run_rpir4
from components.bb import run_bb
from components.rdht4 import run_rdht4

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
    print('Pi3 is starting')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        #run_b4sd(settings['B4SD'], threads, stop_event)
        #run_ir_receiver(settings['BIR'], threads, stop_event)
        #run_brgb(settings['BRGB'], threads, stop_event)
        #run_rdht4(settings['RDHT4', threads, stop_event])
        # run_bb(settings['BB'], threads, stop_event)
        # run_rpir4(settings['rpir4'], threads, stop_event)


       
        #run_dht(dht1_settings, threads, stop_event)

        input_thread = threading.Thread(target=user_input_thread, args=(input_queue, stop_event,settings))
        input_thread.start()
        threads.append(input_thread)

        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()