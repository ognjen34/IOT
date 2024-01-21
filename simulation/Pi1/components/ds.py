

from simulator.ds import run_ds_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

ds_data = []
counter_lock = threading.Lock()

def publisher_task(event, ds_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = ds_data.copy()
            publish_data_counter = 0
            ds_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published ds values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_data,))
publisher_thread.daemon = True
publisher_thread.start()


def ds_callback(publish_event, db_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Door button {db_settings['name']} was pressed!")
    ds_payload = {
        "measurement": "Button",
        "value": "Door button was pressed!",
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
    }
    with counter_lock:
        ds_data.append(('Button', json.dumps(ds_payload), 0, True))
        publish_event.set()


def run_ds(settings,threads, stop_event):
        if settings['simulated']:
            print("Starting ds sumilator")
            ds_thread = threading.Thread(target = run_ds_simulator, args=(2, ds_callback, stop_event,publish_event,settings))
            ds_thread.start()
            threads.append(ds_thread)
            print("ds sumilator started")
        else:
            from sensors.ds import run_ds_loop, DS
            print("Starting ds loop")
            ds = DS(settings['pin'])
            ds_thread = threading.Thread(target=run_ds_loop, args=(ds, 1, ds_callback, stop_event,publish_event,settings))
            ds_thread.start()
            threads.append(ds_thread)
            print("ds loop started")
