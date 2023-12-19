import threading
from simulator.pir import run_pir_simulator
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

pir_data = []
counter_lock = threading.Lock()

def publisher_task(event, pir_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = pir_data.copy()
            publish_data_counter = 0
            pir_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published db values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_data,))
publisher_thread.daemon = True
publisher_thread.start()

def motion_detected(publish_event, db_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("Detected motion")
    pir_payload = {
        "measurement": "Motion",
        "value": "Motion Detected!",
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
    }
    with counter_lock:
        pir_data.append(('Buzzer', json.dumps(pir_payload), 0, True))
        publish_event.set()
        
def run_pir(settings, threads, stop_event):    
    if settings['simulated']:
        print("Starting {} simulator".format(settings["name"]))
        pir_thread = threading.Thread(target=run_pir_simulator, args=(10, motion_detected, stop_event,publish_event,settings))
        pir_thread.start()
        threads.append(pir_thread)
        print("{0} simulator started".format(settings["name"]))
    else:
        from sensors.pir import run_loop, PIR
        print("Starting {} loop".format(settings["name"]))
        pir = PIR(settings["pin"], settings['name'])
        pir_thread = threading.Thread(target=run_loop, args=(pir, motion_detected, stop_event,publish_event,settings))
        pir_thread.start()
        threads.append(pir_thread)
        print("{} loop started".format(settings["name"]))