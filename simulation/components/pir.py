import threading
from simulator.pir import run_pir_simulator
import time


def motion_detected(name):
    t = time.localtime()
    print("=" * 10 + name + "=" * 10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("Detected motion")
        
def run_pir(settings, threads, stop_event,name):    
    if settings['simulated']:
        print("Starting {} simulator".format(name))
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, motion_detected, stop_event, name))
        pir_thread.start()
        threads.append(pir_thread)
        print("{0} simulator started".format(name))
    else:
        from sensors.pir import run_pir_loop, PIR
        print("Starting {} loop".format(name))
        pir = PIR(settings["pin"], settings['name'])
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, motion_detected, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
        print("{} loop started".format(name))