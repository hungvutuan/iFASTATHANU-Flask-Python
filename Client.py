# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'

import paho.mqtt.client as mqtt
import json
import time

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45

# The callback for when the client receives a CONNACK response from the server.
sensor_data = {'lpg': 0, 'smoke': 0, 'temperature': 0}
sensor_data_container = []


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CoreElectronics/kitchen")
    # client.subscribe("CoreElectronics/bedroom")


# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic)
    msg.payload = msg.payload.decode("utf-8")
    # print(msg.payload) # <- do you mean this payload = {...} ?
    payload = json.loads(msg.payload)  # you can use json.loads to convert string to json
    sensor_data['lpg'] = payload['lpg']
    sensor_data['smoke'] = payload['smoke']
    sensor_data['temperature'] = payload['temperature']
    print(sensor_data)  # then you can check the value
    sensor_data_container.append(sensor_data)
    client.disconnect()  # Got message then disconnect


# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
# client.loop_forever()

client.loop_start()
client.connect("test.mosquitto.org", 1883, 60)
time.sleep(3.5)
client.disconnect()  # disconnect
client.loop_stop()  # stop loop


def get_sensor_data(*args):
    if args is None:
        return sensor_data_container
    else:
        return sensor_data_container[args[0]]
