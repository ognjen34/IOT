import threading
import time
from simulator.dl import run_dl_simulator
import threading

def dl_callback(status):
    t = time.localtime()
    with threading.Lock():
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Status: {status}")


def run_dl(settings, threads, stop_event, input_queue):
    if settings['simulated']:
        with threading.Lock():
            print("Starting dl sumilator")
        dl_thread = threading.Thread(target = run_dl_simulator, args=(input_queue, 2, dl_callback, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        with threading.Lock():
            print(f"dl sumilator started")
    else:
        from sensors.dl import run_dl_loop, DL
        with threading.Lock():
            print("Starting dl loop")
        uds = DL(settings['trig'], settings["echo"])
        dl_thread = threading.Thread(target=run_dl_loop, args=(input_queue, uds, 2, dl_callback, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        with threading.Lock():
            print("dl loop started")