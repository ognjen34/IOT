

from simulator.dus import run_dus_simulator
import threading
import time
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json


dus_data = []
counter_lock = threading.Lock()

def publisher_task(event, dus_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = dus_data.copy()
            publish_data_counter = 0
            dus_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published db values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dus_data,))
publisher_thread.daemon = True
publisher_thread.start()


def dus_callback(distance,publish_event, db_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Distance: {distance}m")
    dus_payload = {
        "measurement": "Distance",
        "value": distance,
        "simulated": db_settings['simulated'],
        "runs_on": db_settings["runs_on"],
        "name": db_settings["name"],
    }
    with counter_lock:
        dus_data.append(('Distance', json.dumps(dus_payload), 0, True))
        publish_event.set()



def run_dus(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dht1 sumilator")
            dus1_thread = threading.Thread(target = run_dus_simulator, args=(dus_callback, stop_event,publish_event,settings))
            dus1_thread.start()
            threads.append(dus1_thread)
            print("Dus sumilator started")
        else:
            from sensors.dus import run_dus_loop, DUS
            print("Starting dht1 loop")
            dus = DUS(settings['triger_pin'],settings['echo_pin'])
            dus_thread = threading.Thread(target=run_dus_loop, args=(dus, dus_callback, stop_event,publish_event,settings))
            dus_thread.start()
            threads.append(dus_thread)
            print("Dht1 loop started")
