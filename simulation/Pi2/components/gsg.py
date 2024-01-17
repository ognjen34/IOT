

from simulator.gsg import run_gsg_simulator
import threading
import time
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json


gsg_data = []
counter_lock = threading.Lock()

def publisher_task(event, gsg_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gsg_batch = gsg_data.copy()
            publish_data_counter = 0
            gsg_data.clear()
        publish.multiple(local_gsg_batch, hostname=HOSTNAME, port=PORT)
        print(f'published gsg values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gsg_data,))
publisher_thread.daemon = True
publisher_thread.start()


def gsg_callback(read, publish_event, gsg_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"accel: {read[0]}")
        print(f"gyro: {read[1]}")

    acceleration_payload = {
        "measurement": "Acceleration",
        "simulated": gsg_settings['simulated'],
        "runs_on": gsg_settings["runs_on"],
        "name": gsg_settings["name"],
        "value": str(read[0])
    }
    print(read)

    gyro_payload = {
        "measurement": "Gyro",
        "simulated": gsg_settings['simulated'],
        "runs_on": gsg_settings["runs_on"],
        "name": gsg_settings["name"],
        "value": str(read[1])
    }
    with counter_lock:

        gsg_data.append(('Acceleration', json.dumps(acceleration_payload), 0, True))
        gsg_data.append(('Gyro', json.dumps(gyro_payload), 0, True))

        publish_event.set()


def run_gsg(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting gsg sumilator")
            gsg_thread = threading.Thread(target = run_gsg_simulator, args=(10, gsg_callback, stop_event,publish_event,settings))
            gsg_thread.start()
            threads.append(gsg_thread)
            print("gsg sumilator started")
        else:
            from sensors.MPU6050.gyro import run_gyro_loop, GYRO
            print("Starting gsg loop")
            gsg = GYRO()
            gsg_thread = threading.Thread(target=run_gyro_loop, args=(gsg, 2, gsg_callback, stop_event,publish_event,settings))
            gsg_thread.start()
            threads.append(gsg_thread)
            print("gsg loop started")
