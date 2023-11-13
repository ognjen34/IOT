import threading
import time
from simulator.dms import run_dms_simualtor

def dms_callback(keyboard_input, name):
    t = time.localtime()
    print("="*10, end=" ")
    print(name, end=" ")
    print("="*10)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f'Pressed key: {keyboard_input}\n')
    

def run_dms(settings, threads, stop_event, name):
    if settings['simulated']:
        print(f"Starting {name} sumilator")
        ms_thread = threading.Thread(target = run_dms_simualtor, args=(2, dms_callback, name, stop_event))
        ms_thread.start()
        threads.append(ms_thread)
        print(f"{name} sumilator started")
    else:
        from sensors.dms import run_ms_loop, DMS
        print(f"Starting {name} loop")
        ms = DMS(settings, name)
        ms_thread = threading.Thread(target=run_ms_loop, args=(ms, 2, dms_callback, stop_event))
        ms_thread.start()
        threads.append(ms_thread)
        print(f"{name} loop started")