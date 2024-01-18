from simulator.rdht3 import run_rdht3_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


rdht3_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, rdht3_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rdht3_batch = rdht3_batch.copy()
            publish_data_counter = 0
            rdht3_batch.clear()
        publish.multiple(local_rdht3_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} rdht3 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rdht3_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rdht3_callback(humidity, temperature, publish_event, rdht3_settings, code="DHTLIB_OK", verbose=False):
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
        "simulated": rdht3_settings['simulated'],
        "runs_on": rdht3_settings["runs_on"],
        "name": rdht3_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": rdht3_settings['simulated'],
        "runs_on": rdht3_settings["runs_on"],
        "name": rdht3_settings["name"],
        "value": humidity
    }

    with counter_lock:
        rdht3_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        rdht3_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rdht3(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting rdht3 sumilator")
        rdht3_thread = threading.Thread(target = run_rdht3_simulator, args=(2, rdht3_callback, stop_event, publish_event, settings))
        rdht3_thread.start()
        threads.append(rdht3_thread)
        print("rdht3 sumilator started")
    else:
        from sensors.rdht3 import run_rdht3_loop, RDHT3
        print("Starting rdht3 loop")
        rdht3 = RDHT3(settings['pin'])
        rdht3_thread = threading.Thread(target=run_rdht3_loop, args=(rdht3, 2, rdht3_callback, stop_event, publish_event, settings))
        rdht3_thread.start()
        threads.append(rdht3_thread)
        print("rdht3 loop started")
