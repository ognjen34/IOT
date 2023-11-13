

from simulator.ds import run_ds_simulator
import threading
import time

def ds_callback(name,code):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Door button {name} was pressed!")


def run_ds(settings, name,threads, stop_event):
        if settings['simulated']:
            print("Starting ds sumilator")
            ds_thread = threading.Thread(target = run_ds_simulator, args=(2, ds_callback,name, stop_event))
            ds_thread.start()
            threads.append(ds_thread)
            print("ds sumilator started")
        else:
            from sensors.ds import run_ds_loop, DS
            print("Starting ds loop")
            ds = DS(settings['pin'])
            ds_thread = threading.Thread(target=run_ds_loop, args=(ds,name, 2, ds_callback, stop_event))
            ds_thread.start()
            threads.append(ds_thread)
            print("ds loop started")
