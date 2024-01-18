import threading
from simulator.rpir3 import run_rpir3_simulator
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

rpir3_data = []
counter_lock = threading.Lock()

def publisher_task(event, rpir3_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = rpir3_data.copy()
            publish_data_counter = 0
            rpir3_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published db values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rpir3_data,))
publisher_thread.daemon = True
publisher_thread.start()

def motion_detected(publish_event, db_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("Detected motion")
    rpir3_payload = {
        "measurement": "Motion",
        "value": "Motion Detected!",
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
    }
    with counter_lock:
        rpir3_data.append(('Buzzer', json.dumps(rpir3_payload), 0, True))
        publish_event.set()
        
def run_rpir3(settings, threads, stop_event):    
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        rpir3_thread = threading.Thread(target=run_rpir3_simulator, args=(10, motion_detected, stop_event,publish_event,settings))
        rpir3_thread.start()
        threads.append(rpir3_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.rpir3 import run_loop, RPIR3
        print("Starting {} loop".format(settings["name"]))
        rpir3 = RPIR3(settings["pin"], settings['name'])
        rpir3_thread = threading.Thread(target=run_loop, args=(rpir3, motion_detected, stop_event,publish_event,settings))
        rpir3_thread.start()
        threads.append(rpir3_thread)
        print("{} loop started".format(settings["name"]))