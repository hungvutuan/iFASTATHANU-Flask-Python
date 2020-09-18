import os
import sys
import threading

import matplotlib.pyplot as plt
from pyfcm import FCMNotification

import numpy as np
from bin import global_var as VAR

# open the trained file
f = open(VAR.TRAINED_DATA_FILE, "r")
f = f.read().split("|")

# retrieve data from the "trained data file"
weight = np.fromstring(f[0], dtype=float, sep=" ")  # convert weight (string) to a vector
weight = np.reshape(weight, (-1, 2))  # convert vector to a 2D array
bias = np.fromstring(f[1], dtype=float, sep=" ")  # convert bias (string) to a vector

x = np.array(np.zeros(weight.shape))
prediction = np.array(np.zeros(weight.shape[0]))
holder = 0


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def __calc(val):
    count = [0, 0]
    for row in range(weight.shape[0]):
        count[0] = count[0] + val[0] * weight[row][0]
        count[1] = count[1] + val[1] * weight[row][1]

    return count[0] + count[1]


def feed(val):
    total = sigmoid(val[0] * weight[-1][0] + bias[0]) + \
            sigmoid(val[1] * weight[-1][1] + bias[1]) * 100
    res = (total - 75) * 4
    if res < 0:
        return 0
    if res > 100:
        return 100
    return res


fire_val = [55, 16]
neutral_val = [22, -2]
not_fire_val = [-30, -6]
prediction = np.reshape(prediction, (len(prediction), -1))

# for i in range(x.shape[0]):
#     for k in range(x.shape[1]):
#         x[i][k] = sigmoid(x_orig[i][k] * weight[i][k] + bias[k])
#
#     prediction[i] = sigmoid(x[i][0] + x[i][1])


# plt.plot(x_orig[:prediction.shape[0]], sigmoid(x_orig[:prediction.shape[0]]))
# plt.plot(x_orig[:prediction.shape[0]], x)
# plt.title("Sigmoid for accuracy")
# plt.show()

# print("Fire:", feed(fire_val))
# print("Fire1:", feed([10, 8]))
# print("Neutral:", feed(neutral_val))
# print("Not fire:", feed(not_fire_val), "\n")


def check_input(val: dict):
    for room, info in val.items():
        metrics = metrics_dict_to_list(info)
        chance = feed(metrics)
        print(room + ":", metrics, "chance:", chance)
        if chance > VAR.FIRE_BAR:
            send_noti(room, metrics, chance)
            # todo
            # insert to database history a fire


def send_noti(room, metrics: list, chance):
    """Declare a FCMNotification instance, which is then packed
     with a body to send to the Firebase broker"""
    push_service = FCMNotification(
        api_key="AAAAh8zZKmc:APA91bHCM7OfYaJZUAPA"
                "-GVGTPpQMYpbi1RBIWCf4CtBAwpTArWQ_Na0Kla2PX7frNWBqnRtOQqb"
                "Gq4khJVzgSheNQguJFjLpLKxrrH7nPjJwuzrpzN1J8NGztJ-NYyb-DEYI_8Ef5lB")

    # attributes for the notification
    message_title = "Fire Hazard"
    message_body = "from your " + room + " was detected"
    data_message = {
        "chance": chance,
        "temperature": metrics[0],
        "smoke": metrics[1],
        "room": room
    }

    # send the notification to the mobile device(s)
    push_service.notify_topic_subscribers(
        topic_name="fireDetection",
        message_title=message_title,
        message_body=message_body,
        data_message=data_message
    )
    print("Alert sent")
    return 1


def live_percentage(room, sensor_data):
    """Return: The fire possibility of the param room"""
    return {
        room: int(feed(metrics_dict_to_list(sensor_data)))
    }


def feedback(temp, smoke, status):
    return 0


def mean_live_percentage(*sensor):
    """Return: the mean of all fire possibilities of all sensors"""
    sum = 0
    for s in sensor:
        sum += feed(metrics_dict_to_list(s))

    return int(sum/len(sensor))

def metrics_dict_to_list(s):
    """Used to convert metrics from dictionary to list and subtract with offset.
    Input: {
        "smoke" : smoke,
        "temperature": temp
        }
    Output: [smoke - offset, temp - offset]
    Purpose: alter the input to pass as param of the feed() function
    """
    return [s["smoke"] - VAR.SMOKE_OFFSET, s["temperature"] - VAR.TEMP_OFFSET]