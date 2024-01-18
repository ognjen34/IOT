from simulator.rdht1 import run_rdht1_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


rdht1_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, rdht1_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rdht1_batch = rdht1_batch.copy()
            publish_data_counter = 0
            rdht1_batch.clear()
        publish.multiple(local_rdht1_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} rdht1 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rdht1_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rdht1_callback(humidity, temperature, publish_event, rdht1_settings, code="rdht1LIB_OK", verbose=False):
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
        "simulated": rdht1_settings['simulated'],
        "runs_on": rdht1_settings["runs_on"],
        "name": rdht1_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": rdht1_settings['simulated'],
        "runs_on": rdht1_settings["runs_on"],
        "name": rdht1_settings["name"],
        "value": humidity
    }

    with counter_lock:
        rdht1_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        rdht1_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rdht1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting rdht1 sumilator")
        rdht1_thread = threading.Thread(target = run_rdht1_simulator, args=(2, rdht1_callback, stop_event, publish_event, settings))
        rdht1_thread.start()
        threads.append(rdht1_thread)
        print("rdht1 sumilator started")
    else:
        from sensors.rdht1 import run_dht_loop, RDHT1
        print("Starting rdht1 loop")
        rdht1 = RDHT1(settings['pin'])
        rdht1_thread = threading.Thread(target=run_dht_loop, args=(rdht1, 2, rdht1_callback, stop_event, publish_event, settings))
        rdht1_thread.start()
        threads.append(rdht1_thread)
        print("rdht1 loop started")
