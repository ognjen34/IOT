from simulator.gdht import run_gdht_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT


gdht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, gdht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gdht_batch = gdht_batch.copy()
            publish_data_counter = 0
            gdht_batch.clear()
        publish.multiple(local_gdht_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} gdht values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gdht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def gdht_callback(humidity, temperature, publish_event, gdht_settings, code="DHTLIB_OK", verbose=False):
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
        "simulated": gdht_settings['simulated'],
        "runs_on": gdht_settings["runs_on"],
        "name": gdht_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": gdht_settings['simulated'],
        "runs_on": gdht_settings["runs_on"],
        "name": gdht_settings["name"],
        "value": humidity
    }

    with counter_lock:
        gdht_batch.append(('Temperature', json.dumps(temp_payload), 0, True))
        gdht_batch.append(('Humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_gdht(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting gdht sumilator")
        gdht_thread = threading.Thread(target = run_gdht_simulator, args=(2, gdht_callback, stop_event, publish_event, settings))
        gdht_thread.start()
        threads.append(gdht_thread)
        print("gdht sumilator started")
    else:
        from sensors.gdht import run_gdht_loop, GDHT
        print("Starting gdht loop")
        gdht = GDHT(settings['pin'])
        gdht_thread = threading.Thread(target=run_gdht_loop, args=(gdht, 2, gdht_callback, stop_event, publish_event, settings))
        gdht_thread.start()
        threads.append(gdht_thread)
        print("gdht loop started")
