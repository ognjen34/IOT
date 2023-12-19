import threading
import time
from simulator.dms import run_dms_simualtor
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

dms_data = []
counter_lock = threading.Lock()

def publisher_task(event, db_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = db_data.copy()
            publish_data_counter = 0
            db_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published dms values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dms_data,))
publisher_thread.daemon = True
publisher_thread.start()

def dms_callback(keyboard_input,publish_event, db_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print("="*10, end=" ")
        print("="*10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f'Pressed key: {keyboard_input}\n')
    dms_payload = {
        "measurement": "Keystroke",
        "value": keyboard_input,
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
    }
    with counter_lock:
        dms_data.append(('Keystroke', json.dumps(dms_payload), 0, True))
        publish_event.set()
    

def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        with threading.Lock():
            print(f"Starting {settings['name']} sumilator")
        ms_thread = threading.Thread(target = run_dms_simualtor, args=(2, dms_callback, stop_event,publish_event,settings))
        ms_thread.start()
        threads.append(ms_thread)
        with threading.Lock():
            print(f"{settings['name']} sumilator started")
    else:
        from sensors.dms import run_dms_loop, DMS
        print(f"Starting {settings['name']} loop")
        ms = DMS(settings)
        ms_thread = threading.Thread(target=run_dms_loop, args=(ms, 2, dms_callback, stop_event,publish_event,settings))
        ms_thread.start()
        threads.append(ms_thread)
        with threading.Lock():
            print(f"{settings['name']} loop started")