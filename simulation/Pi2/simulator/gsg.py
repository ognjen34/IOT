import time
import random

def generate_sensor_values():
   while True:
        accel_x = random.uniform(-1, 1)
        accel_y = random.uniform(-1, 1)
        accel_z = random.uniform(-1, 1)

        gyro_x = random.uniform(-1, 1)
        gyro_y = random.uniform(-1, 1)
        gyro_z = random.uniform(-1, 1)

        normalized_accel = (accel_x / 16384.0, accel_y / 16384.0, accel_z / 16384.0)
        normalized_gyro = (gyro_x / 131.0, gyro_y / 131.0, gyro_z / 131.0)

        yield [normalized_accel, normalized_gyro]

def run_gsg_simulator(delay, callback, stop_event, publish_event, settings):
    for sensor_data in generate_sensor_values():
        time.sleep(delay)
        callback(sensor_data, publish_event, settings)
        if stop_event.is_set():
            break
