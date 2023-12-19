import threading
import time
from simulator.dl import run_dl_simulator
import threading
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


dl_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()


def publisher_task(event, dl_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = dl_batch.copy()
            publish_data_counter = 0
            dl_batch.clear()
        publish.multiple(local_dl_batch, hostname=HOSTNAME, port=PORT)
        print(f'published  dl values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dl_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dl_callback(status,publish_event, dl_settings, code="DHTLIB_OK", verbose=False):

    if verbose:
        t = time.localtime()
        with threading.Lock():
            print("="*20)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Status: {status}")
    dl_payload = {
        "measurement": "DoorLight",
        "value": status,
        "simulated": dl_settings['simulated'],
        "runs_on": dl_settings["runs_on"],
        "name": dl_settings["name"],
    }
    with counter_lock:
        dl_batch.append(('DoorLight', json.dumps(dl_payload), 0, True))
        publish_event.set()


def run_dl(settings, threads, stop_event, input_queue):
    if settings['simulated']:
        print("Starting dl sumilator")
        dl_thread = threading.Thread(target = run_dl_simulator, args=(input_queue, 2, dl_callback, stop_event,publish_event,settings))
        dl_thread.start()
        threads.append(dl_thread)
        print(f"dl sumilator started")
    else:
        from sensors.dl import run_dl_loop, DL
        print("Starting dl loop")
        uds = DL(settings['trig'], settings["echo"])
        dl_thread = threading.Thread(target=run_dl_loop, args=(input_queue, uds, 2, dl_callback, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        print("dl loop started")