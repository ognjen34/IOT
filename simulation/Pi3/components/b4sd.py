from datetime import datetime
import threading
from simulator.b4sd import run_b4sd_simulator
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

b4sd_data = []
counter_lock = threading.Lock()

def publisher_task(event, b4sd_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_b4sd_batch = b4sd_data.copy()
            publish_data_counter = 0
            b4sd_data.clear()
        publish.multiple(local_b4sd_batch, hostname=HOSTNAME, port=PORT)
        print(f'published b4sd values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, b4sd_data,))
publisher_thread.daemon = True
publisher_thread.start()

def b4sd_callback(settings, s, publish_event):
    t = datetime.now()
    print("="*20)
    print({"timestamp": t, "name": settings['name'], "time_4d": s})
    payload ={
        "measurement": settings['code'],
        "value": s,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
    } 
    with counter_lock:
        b4sd_data.append(('B4SD', json.dumps(payload), 0, True))
        publish_event.set()
    
def run_b4sd(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting b4sd simulator")
        b4sd_thread = threading.Thread(target=run_b4sd_simulator, args=(settings, stop_event, b4sd_callback, publish_event))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        print("ds simulator started")
    else:
        from sensors.b4sd import B4sd
        print("Starting b4sd loop")
        b4sd = B4sd(settings, stop_event, b4sd_callback)
        b4sd_thread = threading.Thread(target=b4sd.run(), args=(settings, stop_event, b4sd_callback, publish_event))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        print("b4sd loop started")