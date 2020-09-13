# MQTT Publish Demo
# Publish two messages, to two different topics
import json
import random
import paho.mqtt.publish as publish

while True:
    MQTT_MSG = json.dumps({"temperature": random.randint(0, 50), "smoke": random.randint(0, 120)})
    publish.single("CoreElectronics/kitchen", MQTT_MSG, hostname="broker.hivemq.com")
    # publish.single("CoreElectronics/topic", "World!", hostname="test.mosquitto.org")
    # print("Done")
