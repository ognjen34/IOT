import time
import random
import paho.mqtt.client as mqtt
from broker_settings import HOSTNAME
def generate_sensor_values():
   while True:
        accel_x = random.uniform(-50, 50)
        accel_y = random.uniform(-50, 50)
        accel_z = random.uniform(-50, 50)

        gyro_x = random.uniform(-50, 50)
        gyro_y = random.uniform(-50, 50)
        gyro_z = random.uniform(-50, 50)

        normalized_accel = (accel_x / 16384.0, accel_y / 16384.0, accel_z / 16384.0)
        normalized_gyro = (gyro_x / 131.0, gyro_y / 131.0, gyro_z / 131.0)

        yield [normalized_accel, normalized_gyro]

def run_gsg_simulator(delay, callback, stop_event, publish_event, settings):
    threshold = 0.37  # Set your threshold for significant gyroscope movement
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOSTNAME, 1883, 60)
    for sensor_data in generate_sensor_values():
        if any(abs(value) > threshold for value in sensor_data[1]):
            mqtt_client.publish("alarm", "on")
            print("ALARMMM")
        time.sleep(3)
        print(sensor_data)
        callback(sensor_data, publish_event, settings)
        if stop_event.is_set():
            break
