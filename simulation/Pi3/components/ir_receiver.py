from datetime import datetime
import threading
from simulator.ir_reciever import run_ir_receiver_simulator
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

ir_data = []
counter_lock = threading.Lock()

def publisher_task(event, ir_data):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ir_batch = ir_data.copy()
            publish_data_counter = 0
            ir_data.clear()
        publish.multiple(local_ir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published ir values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ir_data))
publisher_thread.daemon = True
publisher_thread.start()


def ir_receiver_callback(name, settings,button_name, publish_event):
    t = datetime.now()
    # print("="*20)
    # print({"timestamp": t, "name": name, "button": button_name})
    payload ={
        "measurement": settings['code'],
        "value": button_name,
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
    } 
    with counter_lock:
        ir_data.append(('Infrared', json.dumps(payload), 0, True))
        publish_event.set()
    
def run_ir_receiver(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting ir_receiver simulator")
        ir_thread = threading.Thread(target=run_ir_receiver_simulator, args=(ir_receiver_callback, stop_event, settings, publish_event))
        ir_thread.start()
        threads.append(ir_thread)
        print("ir receiver simulation started")
    else:
        from sensors.ir_receiver import IrReceiver
        print("Starting ir receiver loop")
        ir = IrReceiver(settings, stop_event, ir_receiver_callback, publish_event)
        ir_thread = threading.Thread(target=ir.run(), args=())
        ir_thread.start()
        threads.append(ir_thread)
        print("ir receiver loop started")

        