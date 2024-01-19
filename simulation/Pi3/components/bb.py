

from simulator.bb import run_bb_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

bb_data = []
counter_lock = threading.Lock()

def publisher_task(event, bb_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = bb_data.copy()
            publish_data_counter = 0
            bb_data.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published db values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, bb_data,))
publisher_thread.daemon = True
publisher_thread.start()


def bb_callback(action,publish_event, bb_settings, code="DHTLIB_OK", verbose=False):
    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        if action == "on" :
            print(f"Buzzer started to buzz..")
        else :
            print(f"Buzzer stopped to buzz..")
    bb_payload = {
        "measurement": "Buzzing",
        "value": action,
        "simulated": bb_settings['simulated'],
        "runs_on": bb_settings["runs_on"],
        "name": bb_settings["name"],
    }
    with counter_lock:
        bb_data.append(('Buzzer', json.dumps(bb_payload), 0, True))
        publish_event.set()



    

def run_bb(settings, threads, stop_event,queue):
        if settings['simulated']:
            with threading.Lock():
                print("Starting db sumilator")
            db_thread = threading.Thread(target = run_bb_simulator, args=(queue,1000, bb_callback, stop_event,publish_event,settings))
            db_thread.start()
            threads.append(db_thread)
            with threading.Lock():
                print("db sumilator started")
        else:
            from sensors.db import run_bb_loop, BB
            with threading.Lock():
                print("Starting db loop")
            db = BB(settings['pin'])
            db_thread = threading.Thread(target=run_bb_loop, args=(db, 1000,0.5,2, bb_callback, stop_event,queue,publish_event,settings))
            db_thread.start()
            threads.append(db_thread)
            with threading.Lock():
                print("db loop started")
