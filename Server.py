# MQTT Publish Demo
# Publish two messages, to two different topics
import json
import random
import time

import paho.mqtt.publish as publish

while True:
    MQTT_MSG = json.dumps({
        "temperature": random.randint(45, 50),
        "smoke": random.randint(90, 120)
    })
    MQTT_MSG1 = json.dumps({
        "temperature": random.randint(45, 50),
        "smoke": random.randint(90, 120)
    })
    MQTT_MSG2 = json.dumps({
        "temperature": random.randint(45, 50),
        "smoke": random.randint(90, 120)
    })

    publish.single("CoreElectronics/kitchen", MQTT_MSG, hostname="broker.hivemq.com")
    publish.single("CoreElectronics/bedroom", MQTT_MSG1, hostname="broker.hivemq.com")
    publish.single("CoreElectronics/living", MQTT_MSG2, hostname="broker.hivemq.com")
    time.sleep(1)
    # print("Done")
