

from simulator.dus import run_dus_simulator
import threading
import time

def dus_callback(distance, code):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Distance: {distance}m")



def run_dus(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dht1 sumilator")
            dus1_thread = threading.Thread(target = run_dus_simulator, args=(2, dus_callback, stop_event))
            dus1_thread.start()
            threads.append(dus1_thread)
            print("Dus sumilator started")
        else:
            from sensors.dus import run_dus_loop, DUS
            print("Starting dht1 loop")
            dus = DUS(settings['triger_pin'],settings['echo_pin'])
            dus_thread = threading.Thread(target=run_dus_loop, args=(dus, 2, dus_callback, stop_event))
            dus_thread.start()
            threads.append(dus_thread)
            print("Dht1 loop started")
