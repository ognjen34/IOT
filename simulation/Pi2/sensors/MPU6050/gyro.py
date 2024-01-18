#!/usr/bin/env python3
from .MPU6050 import MPU6050
import time
import os

class GYRO(object) :
    def __init__(self):
        self.mpu = MPU6050()     
        self.accel = [0]*3               
        self.gyro = [0]*3                
        self.mpu.dmp_initialize()    
            
    def read(self):
        self.accel = self.mpu.get_acceleration()  
        self.gyro = self.mpu.get_rotation()  
        return [(self.accel[0] / 16384.0, self.accel[1] / 16384.0, self.accel[2] / 16384.0),
                (self.gyro[0] / 131.0, self.gyro[1] / 131.0, self.gyro[2] / 131.0)]
        


def run_gyro_loop(gyro, delay, callback, stop_event,publish_event,settings):
		while True:
			read = gyro.read()
			callback(read,publish_event,settings)
			if stop_event.is_set():
					break
			time.sleep(delay)

