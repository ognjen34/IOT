import threading
from simulator.dpir1 import run_dpir1_simulator
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

dpir1_data = []
counter_lock = threading.Lock()

def publisher_task(event, dpir1_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = dpir1_data.copy()
            publish_data_counter = 0
            dpir1_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published db values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dpir1_data,))
publisher_thread.daemon = True
publisher_thread.start()

def motion_detected(publish_event, db_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("Detected motion")
    dpir1_payload = {
        "measurement": "Motion",
        "value": "Motion Detected!",
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
    }
    with counter_lock:
        dpir1_data.append(('Buzzer', json.dumps(dpir1_payload), 0, True))
        publish_event.set()
        
def run_dpir1(settings, threads, stop_event):    
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        dpir1_thread = threading.Thread(target=run_dpir1_simulator, args=(10, motion_detected, stop_event,publish_event,settings))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.dpir1 import run_loop, DPIR1
        print("Starting {} loop".format(settings["name"]))
        dpir1 = DPIR1(settings["pin"], settings['name'])
        dpir1_thread = threading.Thread(target=run_loop, args=(dpir1, motion_detected, stop_event,publish_event,settings))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("{} loop started".format(settings["name"]))