from datetime import datetime
import threading
from simulator.brgb import run_brgb_simulator

def brgb_callback(settings, button_name):
    t = datetime.now()
    print("="*20)
    print({"timestamp": t, "name": settings['name'], "mode": button_name})
    
def run_brgb(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting brgb simulator")
        brgb_thread = threading.Thread(target=run_brgb_simulator, args=(settings, brgb_callback, stop_event))
        brgb_thread.start()
        threads.append(brgb_thread)
        print("b4sd simulator started ")
    else:
        from sensors.brgb import Brgb
        print("Starting brgb loop")
