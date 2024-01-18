from simulator.rdht2 import run_rdht2_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


rdht2_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, rdht2_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rdht2_batch = rdht2_batch.copy()
            publish_data_counter = 0
            rdht2_batch.clear()
        publish.multiple(local_rdht2_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} rdht2 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rdht2_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rdht2_callback(humidity, temperature, publish_event, rdht2_settings, code="rdht2LIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    temp_payload = {
        "measurement": "Temperature",
        "simulated": rdht2_settings['simulated'],
        "runs_on": rdht2_settings["runs_on"],
        "name": rdht2_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": rdht2_settings['simulated'],
        "runs_on": rdht2_settings["runs_on"],
        "name": rdht2_settings["name"],
        "value": humidity
    }

    with counter_lock:
        rdht2_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        rdht2_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rdht2(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting rdht2 sumilator")
        rdht2_thread = threading.Thread(target = run_rdht2_simulator, args=(2, rdht2_callback, stop_event, publish_event, settings))
        rdht2_thread.start()
        threads.append(rdht2_thread)
        print("rdht2 sumilator started")
    else:
        from sensors.rdht2 import run_dht_loop, RDHT2
        print("Starting rdht2 loop")
        rdht2 = RDHT2(settings['pin'])
        rdht2_thread = threading.Thread(target=run_dht_loop, args=(rdht2, 2, rdht2_callback, stop_event, publish_event, settings))
        rdht2_thread.start()
        threads.append(rdht2_thread)
        print("rdht2 loop started")
