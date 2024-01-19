from simulator.rdht4 import run_rdht4_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


rdht4_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, rdht4_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rdht4_batch = rdht4_batch.copy()
            publish_data_counter = 0
            rdht4_batch.clear()
        publish.multiple(local_rdht4_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} rdht4 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rdht4_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rdht4_callback(humidity, temperature, publish_event, rdht4_settings, code="rdht4LIB_OK", verbose=False):
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
        "simulated": rdht4_settings['simulated'],
        "runs_on": rdht4_settings["runs_on"],
        "name": rdht4_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": rdht4_settings['simulated'],
        "runs_on": rdht4_settings["runs_on"],
        "name": rdht4_settings["name"],
        "value": humidity
    }

    with counter_lock:
        rdht4_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        rdht4_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rdht4(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting rdht4 sumilator")
        rdht4_thread = threading.Thread(target = run_rdht4_simulator, args=(2, rdht4_callback, stop_event, publish_event, settings))
        rdht4_thread.start()
        threads.append(rdht4_thread)
        print("rdht4 sumilator started")
    else:
        from sensors.rdht4 import run_dht_loop, RDHT4
        print("Starting rdht4 loop")
        rdht4 = RDHT4(settings['pin'])
        rdht4_thread = threading.Thread(target=run_dht_loop, args=(rdht4, 2, rdht4_callback, stop_event, publish_event, settings))
        rdht4_thread.start()
        threads.append(rdht4_thread)
        print("rdht4 loop started")
