import os
import sys
import threading
from shutil import copyfile, SameFileError

import matplotlib.pyplot as plt
from pyfcm import FCMNotification

import numpy as np
from bin import global_var as VAR
from AI import logistic_model as model
import time

renew = False

# open the trained file
work_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
f = open(work_dir + "/" + VAR.TRAINED_DATA_FILE, "r")
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
            # todo insert to database history a fire

            # todo add reading to dataset
            f = open(work_dir + VAR.FIRE_DATASET, 'a')
            f.write('0, ' + str(metrics[0] + ', ' + str(metrics[1])))
        elif chance < VAR.IMMINENT_BAR:
            nf = open(work_dir + VAR.NON_FIRE_DATASET, 'a')
            nf.write('0, ' + str(metrics[0] + ', ' + str(metrics[1])))


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
    if room == "living":
        message_body = "from your " + room + "room was detected"
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


def mean_live_percentage(*sensor):
    """Return: the mean of all fire possibilities of all sensors"""
    sum_chance = 0
    for s in sensor:
        sum_chance += feed(metrics_dict_to_list(s))

    return int(sum_chance / len(sensor))


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


class ChangeDatasetError(Exception):
    """Error caught only when attempting to change dataset with user's feedback"""

    def __init__(self, stack_trace, loc):
        if loc is not None:
            self.loc = loc
        else:
            self.loc = "Unknown"
        self.type = "[ERROR]"
        self.info = "Error while changing dataset"
        self.stack_trace = stack_trace
        print(self.type, self.info, "\n\t" + "Stack Trace:", self.stack_trace, "\n\tLocation:", loc)


def copy_file(src, dst):
    """Copy the contents of file src to the new location dst"""
    try:
        copyfile(src, dst)
    except (SameFileError, IOError):
        print("Cannot copy the", VAR.TRAINED_DATA_FILE, "file")
        return VAR.ERROR_CODE


def feedback(data):
    """Receives the feedback of user"""
    temp = data['temperature']
    smoke = data['smoke']

    res = change_dataset(temp, smoke)
    if res:
        return True
    return False


def change_dataset(temp, smoke):
    """Change the dataset when user sends a feedback about wrong attempt to alert fire
    The contents that are changed are readings in the fire dataset that BOTH have
        - the temperature reading
        - the smoke reading
    within the proximity of the attempted alarm. The "proximity" implied here is not a fixed value.

    Input: temperature and smoke from the attempted alert
    Output: True if the contents of the dataset are changed
    """
    under_bound_temp = temp - 1
    upper_bound_temp = temp + 1

    under_bound_smoke = smoke - 2
    upper_bound_smoke = smoke + 2

    fire = open(work_dir + "/Dataset/fire.csv", "r").read()
    non_fire = open(work_dir + "/Dataset/non-fire.csv", "r").read()
    mover = []

    fire = fire.split('\n')
    non_fire = non_fire.split("\n")
    count = 0

    # find the corresponding values in the fire dataset
    i = 0
    for row in fire:
        if row == '' or row is None:
            continue
        r = row.split(",")
        try:
            if under_bound_smoke < int(float(r[1])) < upper_bound_smoke and under_bound_temp < int(
                    float(r[2])) < upper_bound_temp:
                mover.append(fire.pop(i))
            else:
                count += 1
        except Exception as e:
            raise ChangeDatasetError(e, count)
        i += 1

    # trim the blank values at the end of both dataset
    while non_fire[-1] == '' or non_fire[-1] is None:
        non_fire.pop()
    while fire[-1] == '' or fire[-1] is None:
        fire.pop()

    # and moves those values to the non_fire dataset
    for i in range(len(mover)):
        non_fire.append(mover[i])

    # backup the original dataset
    copy_file(work_dir + VAR.FIRE_DATASET, work_dir + VAR.FIRE_DATASET + "_backup.txt")
    copy_file(work_dir + VAR.NON_FIRE_DATASET, work_dir + VAR.NON_FIRE_DATASET + "_backup.txt")

    # rewrite the contents of the fire and non-fire dataset
    f = open(work_dir + VAR.FIRE_DATASET, "w")
    nf = open(work_dir + VAR.NON_FIRE_DATASET, "w")

    for f_row in fire:
        f.write(f_row + "\n")

    for nf_row in non_fire:
        nf.write(nf_row + "\n")

    f.close()
    nf.close()

    # rerun the training model
    global renew
    renew = True

    return True


class CheckFeedback(threading.Thread):
    """Repeatedly check for renewing the logit model request
    Triggered only when user sends a feedback of FALSE ATTEMPT TO ALARM
    Input: None
    Output: None"""

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            global renew
            if renew:
                try:
                    model.train(isVisualize=False)
                    print(VAR.MESS_SUCCESS, "Re-training succeeded")
                    renew = False
                except Exception:
                    print(VAR.MESS_ERROR, "Re-training failed")


check_feedback = CheckFeedback()
check_feedback.start()
