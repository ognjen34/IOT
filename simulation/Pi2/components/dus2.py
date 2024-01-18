

from simulator.dus2 import run_dus2_simulator
import threading
import time
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json


dus2_data = []
counter_lock = threading.Lock()

def publisher_task(event, dus2_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = dus2_data.copy()
            publish_data_counter = 0
            dus2_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published db values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dus2_data,))
publisher_thread.daemon = True
publisher_thread.start()


def dus2_callback(distance,publish_event, db_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Distance: {distance}m")
    dus2_payload = {
        "measurement": "Distance",
        "value": distance,
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
    }
    with counter_lock:
        dus2_data.append(('Distance', json.dumps(dus2_payload), 0, True))
        publish_event.set()



def run_dus2(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dus2 sumilator")
            dus2_thread = threading.Thread(target = run_dus2_simulator, args=(10, dus2_callback, stop_event,publish_event,settings))
            dus2_thread.start()
            threads.append(dus2_thread)
            print("dus2 sumilator started")
        else:
            from sensors.dus2 import run_dus2_loop, DUS2
            print("Starting dus2 loop")
            dus2 = DUS2(settings['triger_pin'],settings['echo_pin'])
            dus2_thread = threading.Thread(target=run_dus2_loop, args=(dus2, 2, dus2_callback, stop_event,publish_event,settings))
            dus2_thread.start()
            threads.append(dus2_thread)
            print("dus2 loop started")
