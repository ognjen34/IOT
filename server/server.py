from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from flask_cors import CORS  # Import CORS
from flask_socketio import SocketIO, emit  # Import SocketIO


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # "*" allows all origins, replace with your specific origin


# InfluxDB Configuration
# token = "imF1ROkkg2qx5SO_iGok09SliuUbknV-ygt7T_WRzxhOiipjqtsS0AUm7CwSq8tT-Ytx4KhZbTE-jENqEWtWzA=="
token = "oTfxHLqLa5PV0axqZoqvXJf01dK9Q4Tn-6A6aVrHeuQ-CaoaL_EJw5x51KP5o7w9IA5ugYS0FMqrNXXdBUITHA=="
org = "ftn"
url = "http://localhost:8086"
bucket = "iot"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc):
    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("DoorLight")
    client.subscribe("Buzzer")
    client.subscribe("Distance")
    client.subscribe("Keystroke")
    client.subscribe("Button")
    client.subscribe("Acceleration")
    client.subscribe("Gyro")
    client.subscribe("Infrared")
    client.subscribe("alarm")
    client.subscribe("people")
    client.subscribe("rpir")
    client.subscribe("gdht/temperature")
    client.subscribe("gdht/humidity")





mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(msg)
people_inside = 0

def save_to_db(msg):
    global people_inside
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

    if msg.topic == "alarm":
        point = (
            Point("alarm")
            .field("measurement", msg.payload.decode("utf-8"))
        )
        print(point)
        write_api.write(bucket=bucket, org=org, record=point)
        if msg.payload.decode("utf-8") == "on":
            socketio.emit('alarm', "red")
        else :
            socketio.emit('alarm', "blue")


    elif msg.topic == "people":
        people_inside += int(msg.payload.decode("utf-8"))
        if people_inside < 0 :
            people_inside = 0
        point = (
            Point("People")
            .field("measurement", people_inside)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        print(people_inside)
        socketio.emit('people', str(people_inside))
    elif msg.topic == "gdht/humidity" :
        socketio.emit('humidity', str(msg.payload.decode("utf-8")))
    elif msg.topic == "gdht/temperature" :
        socketio.emit('temperature', str(msg.payload.decode("utf-8")))



    elif msg.topic == "rpir" :
        print(people_inside)
        if people_inside == 0 :
            
            mqtt_client.publish("alarm", "on")


    else :
        data = json.loads(msg.payload.decode('utf-8'))
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .field("measurement", data["value"])
        )
        print(point)
        write_api.write(bucket=bucket, org=org, record=point)


# Route to store dummy data
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/brgb', methods=['POST'])
def manage_brgb():
    try:
        data = request.get_json()
        mode = data.get('mode')
        print(mode)
        mqtt_client.publish("brgb", mode)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route('/b4sd', methods=['POST'])
def manage_b4sd():
    try:
        data = request.get_json()
        mode = data.get('mode')
        print(mode)
        mqtt_client.publish("b4sd", mode)
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    
@app.route('/alarmoff', methods=['GET'])
def alarm_off():
    try:
        mqtt_client.publish("alarm", "off")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
      
def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Humidity")"""
    return handle_influx_query(query)


@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Humidity")
    |> mean()"""
    return handle_influx_query(query)


if __name__ == '__main__':
    app.run(debug=True)
