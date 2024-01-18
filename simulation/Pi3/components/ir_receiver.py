from datetime import datetime
import threading
from simulator.ir_reciever import run_ir_receiver_simulator


def ir_receiver_callback(name, button_name):
    t = datetime.now()
    print("="*20)
    print({"timestamp": t, "name": name, "button": button_name})
    
    
def run_ir_receiver(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting ir_receiver simulator")
        ir_thread = threading.Thread(target=run_ir_receiver_simulator, args=(ir_receiver_callback, stop_event, settings['name']))
        ir_thread.start()
        threads.append(ir_thread)
        print("ir receiver simulation started")
    else:
        from sensors.ir_receiver import IrReceiver
        print("Starting ir receiver loop")
        ir = IrReceiver(settings, stop_event, ir_receiver_callback, "publish_event")
        ir_thread = threading.Thread(target=ir.run(), args=())
        ir_thread.start()
        threads.append(ir_thread)
        print("ir receiver loop started")

        