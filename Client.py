# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'

import json
import time

import paho.mqtt.client as mqtt

# csvfile="C:/Users/DELL/Desktop/MQTT/fire.csv"
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45

# The callback for when the client receives a CONNACK response from the server.
sensor_data_kitchen = {'smoke': 0, 'temperature': 0}
sensor_data_bedroom = {'smoke': 0, 'temperature': 0}
sensor_data_living = {'smoke': 0, 'temperature': 0}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CoreElectronics/kitchen")
    client.subscribe("CoreElectronics/bedroom")
    client.subscribe("CoreElectronics/living")


# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    if msg.topic == "CoreElectronics/bedroom":
        msg.payload = msg.payload.decode("utf-8")
        payload = json.loads(msg.payload)  # you can use json.loads to convert string to json
        sensor_data_bedroom['smoke'] = payload['smoke']
        sensor_data_bedroom['temperature'] = payload['temperature']
        # print(sensor_data_bedroom)
        # with open(csvfile, 'a',newline='') as csvfiles:
        # writer = csv.writer(csvfiles,delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        # writer.writerow([sensor_data_bedroom['lpg'],sensor_data_bedroom['smoke'],sensor_data_bedroom['temperature']])
        # csvfiles.close()
        # print(sensor_data_bedroom)

        # f=open(csvfile,'wb') # opens file for writing (erases contents)
        # csv.writer(f, delimiter =' ',quotechar =',',quoting=csv.QUOTE_MINIMAL)

    if msg.topic == "CoreElectronics/kitchen":
        msg.payload = msg.payload.decode("utf-8")
        payload = json.loads(msg.payload)  # you can use json.loads to convert string to json
        sensor_data_kitchen['smoke'] = payload['smoke']
        sensor_data_kitchen['temperature'] = payload['temperature']
        # (sensor_data_kitchen)
        # with open(csvfile, 'a',newline='') as csvfiles:
        #      writer = csv.writer(csvfiles,delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        #      writer.writerow([sensor_data_kitchen['lpg'],sensor_data_kitchen['smoke'],sensor_data_kitchen['temperature']])
        #      csvfiles.close()
    if msg.topic == "CoreElectronics/living":
        msg.payload = msg.payload.decode("utf-8")
        payload = json.loads(msg.payload)  # you can use json.loads to convert string to json
        sensor_data_living['smoke'] = payload['smoke']
        sensor_data_living['temperature'] = payload['temperature']
        # print(sensor_data_living)

    # print(msg.topic)
    # msg.payload = msg.payload.decode("utf-8")
    # print(msg.payload) # <- do you mean this payload = {...} ?
    # payload = json.loads(msg.payload) # you can use json.loads to convert string to json
    # sensor_data['lpg']=payload['lpg']
    # sensor_data['smoke']=payload['smoke']
    # sensor_data['temperature']=payload['temperature']
    # print(sensor_data) # then you can check the value
    # client.disconnect() # Got message then disconnect


# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()


# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
# client.loop_forever()

def getDataKitchen():
    client.loop_start()
    client.connect("test.mosquitto.org", 1883, 60)
    time.sleep(10)
    client.disconnect()  # disconnect
    client.loop_stop()  # stop loop
    return sensor_data_kitchen
