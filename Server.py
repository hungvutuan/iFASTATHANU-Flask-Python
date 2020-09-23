# MQTT Publish Demo
# Publish two messages, to two different topics
import json
import random
import time

import paho.mqtt.publish as publish

while True:
    MQTT_MSG_kitchen = json.dumps({
        "temperature": random.randint(45, 50),
        "smoke": random.randint(90, 120)
    })
    MQTT_MSG_bedroom = json.dumps({
        "temperature": random.randint(35, 36),
        "smoke": random.randint(50, 80)
    })
    MQTT_MSG_livingroom = json.dumps({
        "temperature": random.randint(33, 35),
        "smoke": random.randint(90, 120)
    })

    publish.single("CoreElectronics/kitchen", MQTT_MSG_kitchen, hostname="broker.hivemq.com")
    publish.single("CoreElectronics/bedroom", MQTT_MSG_bedroom, hostname="broker.hivemq.com")
    publish.single("CoreElectronics/living", MQTT_MSG_livingroom, hostname="broker.hivemq.com")
    time.sleep(1)
