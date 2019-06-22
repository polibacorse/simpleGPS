from paho.mqtt import client as mqtt
import json
import pynmea2
import serial
import time

client = mqtt.Client("GPS Reader")
client.connect("localhost")


device = serial.Serial('/dev/ttyS0', 9600)

while True:
    data_raw = device.readline().rstrip()
    msg = data_raw.decode('ascii', 'ignore')


    if msg.startswith("$GPRMC"):

        data = pynmea2.parse(msg)
        timestamp = int(time.time())
        position = { "latitude": data.latitude, "longitude": data.longitude, "time": timestamp }
        speed = { "speed": data.spd_over_grnd * 1.852, "time": timestamp }

        client.publish("data/formatted/position", json.dumps(position))
        client.publish("data/formatted/speed", json.dumps(speed))



