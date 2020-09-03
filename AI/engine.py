import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import os
import shutil


def append_bias(array, bias: float):
    """Append a vector of [bias] values to the array"""
    vector = np.array([])
    for i in range(array.shape[0]):
        vector = np.append(vector, [bias])
    vector = vector.reshape(array.shape[0], 1)
    return np.append(array, vector, axis=1)


work_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

# Set dataset
fire = np.genfromtxt(work_dir + "/Dataset/fire_1.csv", delimiter=',', )
non_fire = np.genfromtxt(work_dir + "/Dataset/non-fire_1.csv", delimiter=',', )

# add bias term as a vector
bias = 4
fire = append_bias(fire, bias)
non_fire = append_bias(non_fire, bias)

# plot the dataset
s = 60
y = np.array([])
for d1, sample1 in enumerate(fire):
    plt.scatter(sample1[1], sample1[2], s=s, marker='+', linewidths=1)
    y = np.append(y, [1])

for d2, sample2 in enumerate(non_fire):
    plt.scatter(sample2[1], sample2[2], s=s, marker='.', linewidths=1)
    y = np.append(y, [-1])

plt.xlabel('Smoke (PPM)')
plt.ylabel('Temperature (°C)')
plt.clf()

fire = np.delete(fire, 0, 1)
non_fire = np.delete(non_fire, 0, 1)
x = np.append(fire, non_fire, 0)


def svm_sgd_plot(X, Y):
    # Initialize our SVMs weight vector with zeros (3 values)
    weight = np.zeros(len(X[0]))
    # The learning rate
    eta = 0.8
    # how many iterations to train for
    epochs = 6000
    # store misclassifications so we can plot how they change over time
    errors = []
    error_count = 0  # count for misclassified cases over epochs
    # get the time this algorithm was run
    time_format = '%H:%M:%S'
    start_time = time.strftime(time_format, time.localtime())
    # count_epoch = 1
    iter_rate = 0.00185

    # training part, gradient descent part
    print("Training started. \n" +
          "Predicted run time:", time.strftime('%H:%M:%S', time.gmtime(iter_rate * epochs)))
    for epoch in range(1, epochs):
        error = 0
        for i, x in enumerate(X):
            # misclassifications
            if (Y[i] * np.dot(X[i], weight)) < 1:
                # misclassified update for ours weights
                weight = weight + eta * ((X[i] * Y[i]) + (-2 * (1 / epoch) * weight))
                error = 1
            else:
                # correct classification, update our weights
                weight = weight + eta * (-2 * (1 / epoch) * weight)
        if error == 1:
            error_count = error_count + 1
        errors.append(error)

    # get the time the algorithm finishes
    end_time = time.strftime(time_format, time.localtime())

    # get total time the algorithm ran
    print("________________________")
    run_time = datetime.strptime(end_time, time_format) - datetime.strptime(start_time, time_format)
    print("Total run time: ", run_time)
    print("ETA: ", eta)
    print("Epoch: ", epochs)
    accuracy = "{:.2f}".format(((epochs - error_count) / epochs) * 100)
    print("Accuracy: ", str(accuracy) + "%")

    # plot the rate of classification errors during training for our SVM
    plt.plot(errors, '|')
    plt.ylim(0.5, 1.5)
    plt.xlabel('Epoch')
    plt.ylabel('Misclassified')
    plt.title("Misclassified values during Gradient Descent")

    # save file
    file_name = "Gra-" + str(eta).replace(".", "_") + "-" + str(epochs) + ".png"
    plt.savefig(file_name)
    # move to folder Results and overwrite if name exists
    shutil.move(os.path.join("", file_name), os.path.join("./Results/", file_name))

    plt.show()  # display the plot
    return weight


# run the svm algorithm
w = svm_sgd_plot(x, y)

# Print the hyperplane calculated by svm_sgd()
x2 = [w[0], w[1], -w[1], w[0]]
x3 = [w[0], w[1], w[1], -w[0]]

x2x3 = np.array([x2, x3])
X, Y, U, V = zip(*x2x3)
ax = plt.gca()
ax.quiver(X, Y, U, V, scale=1, color='blue')


for d1, sample1 in enumerate(fire):
    plt.scatter(sample1[0], sample1[1], s=s, marker='+', linewidths=1)

for d2, sample2 in enumerate(non_fire):
    plt.scatter(sample2[0], sample2[1], s=s, marker='.', linewidths=1)

plt.xlabel('Smoke (PPM)')
plt.ylabel('Temperature (°C)')
plt.show()
