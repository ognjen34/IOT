

from simulator.ds2 import run_ds2_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

ds2_data = []
counter_lock = threading.Lock()

def publisher_task(event, ds2_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = ds2_data.copy()
            publish_data_counter = 0
            ds2_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published ds2 values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds2_data,))
publisher_thread.daemon = True
publisher_thread.start()


def ds2_callback(publish_event, db_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Door button {db_settings['name']} was pressed!")
    ds2_payload = {
        "measurement": "Button",
        "value": "Door button was pressed!",
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
    }
    with counter_lock:
        ds2_data.append(('Button', json.dumps(ds2_payload), 0, True))
        publish_event.set()


def run_ds2(settings,threads, stop_event):
        if settings['simulated']:
            print("Starting ds2 sumilator")
            ds2_thread = threading.Thread(target = run_ds2_simulator, args=(2, ds2_callback, stop_event,publish_event,settings))
            ds2_thread.start()
            threads.append(ds2_thread)
            print("ds2 sumilator started")
        else:
            from sensors.ds2 import run_ds2_loop, DS2
            print("Starting ds2 loop")
            ds2 = DS2(settings['pin'])
            ds2_thread = threading.Thread(target=run_ds2_loop, args=(ds2, 2, ds2_callback, stop_event,publish_event,settings))
            ds2_thread.start()
            threads.append(ds2_thread)
            print("ds loop started")
