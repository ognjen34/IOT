

from simulator.db import run_db_simulator
import threading
import time

def db_callback(action,code):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    if action == "on" :
        print(f"Buzzer started to buzz..")
    else :
        print(f"Buzzer stopped to buzz..")


    

def run_db(settings, threads, stop_event,queue):
        if settings['simulated']:
            print("Starting db sumilator")
            db_thread = threading.Thread(target = run_db_simulator, args=(queue,1000, db_callback, stop_event))
            db_thread.start()
            threads.append(db_thread)
            print("db sumilator started")
        else:
            from sensors.db import run_db_loop, DB
            print("Starting db loop")
            db = DB(settings['pin'])
            db_thread = threading.Thread(target=run_db_loop, args=(db, 1000,0.1,2, db_callback, stop_event,queue))
            db_thread.start()
            threads.append(db_thread)
            print("db loop started")
