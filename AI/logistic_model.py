# importing modules
import os
import sys
from datetime import datetime, date
from shutil import copyfile, SameFileError

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder

from bin import global_var as VAR


def train(isVisualize, epoch=300, learning_rate=0.3):
    start_time = datetime.now()
    work_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    val = []

    tf.compat.v1.disable_eager_execution()

    # Set dataset
    fire = np.genfromtxt(work_dir + "/Dataset/fire.csv", delimiter=',', )
    non_fire = np.genfromtxt(work_dir + "/Dataset/non-fire.csv", delimiter=',', )

    # Feature Matrix
    fire = np.delete(fire, 0, 1)
    non_fire = np.delete(non_fire, 0, 1)
    x_orig = np.append(fire, non_fire, 0)
    for row in x_orig:
        for col in range(len(row)):
            if col == 0:
                row[col] = row[col] - VAR.SMOKE_OFFSET
            if col == 1:
                row[col] = row[col] - VAR.TEMP_OFFSET

    y_orig = np.array([])

    # Data labels
    for d1, sample1 in enumerate(fire):
        y_orig = np.append(y_orig, [1], 0)

    for d2, sample2 in enumerate(non_fire):
        y_orig = np.append(y_orig, [0], 0)

    y_orig = np.reshape(y_orig, (len(y_orig), -1))

    print("Shape of Feature Matrix:", x_orig.shape)
    print("Shape Label Vector:", y_orig.shape)

    # Positive Data Points
    x_pos = np.array([x_orig[i] for i in range(len(x_orig)) if y_orig[i] == 1])

    # Negative Data Points
    x_neg = np.array([x_orig[i] for i in range(len(x_orig))
                      if y_orig[i] == 0])

    # visualize the dataset on a 2D plot
    if isVisualize:
        visualize_dataset(x_orig, y_orig, original=True)

    # encode with OneHotEncoder
    oneHot = OneHotEncoder()
    oneHot.fit(x_orig)
    x = oneHot.transform(x_orig).toarray()
    oneHot.fit(y_orig)
    y = oneHot.transform(y_orig).toarray()

    alpha, epochs = learning_rate, epoch
    m, n = x.shape
    # display dimensions of the dataset
    print('m =', m)
    print('n =', n)
    print('Learning Rate =', alpha)
    print('Number of Epochs =', epochs)

    # There are n columns in the feature matrix
    # after One Hot Encoding.
    X = tf.compat.v1.placeholder(tf.float32, [None, n])

    # since this is a binary classification problem, Y can take only 2 values.
    Y = tf.compat.v1.placeholder(tf.float32, [None, 2])

    # trainable Variable Weights
    W = tf.Variable(tf.zeros([n, 2]))

    # trainable Variable Bias
    b = tf.Variable(tf.zeros([2]))

    # the primary hypothesis
    Y_hat = tf.nn.sigmoid(tf.add(tf.matmul(X, W), b))

    # Sigmoid Cross Entropy Cost Function
    cost = tf.nn.sigmoid_cross_entropy_with_logits(
        logits=Y_hat, labels=Y)

    # optimize gradient descent
    optimizer = tf.compat.v1.train.GradientDescentOptimizer(
        learning_rate=alpha).minimize(cost)

    init = tf.compat.v1.global_variables_initializer()

    # start the Tensorflow Session
    with tf.compat.v1.Session() as sess:
        # init the variables
        sess.run(init)
        cost_history, accuracy_history = [], []

        for epoch in range(epochs):
            sess.run(optimizer, feed_dict={X: x, Y: y})

            # calculate cost
            c = sess.run(cost, feed_dict={X: x, Y: y})

            # generate accuracy of the current training epoch
            correct_prediction = tf.equal(tf.argmax(Y_hat, 1), tf.argmax(Y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

            # save values to history
            cost_history.append(sum(sum(c)))
            accuracy_history.append(accuracy.eval({X: x, Y: y}) * 100)

            # result on current Epoch
            if epoch % 100 == 0 and epoch != 0:
                print("Epoch " + str(epoch) + " Cost: "
                      + str(cost_history[-1]))

        Weight = sess.run(W)  # optimized weight
        Bias = sess.run(b)  # optimized bias

        # accuracy
        correct_prediction = tf.equal(tf.argmax(Y_hat, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print("\nAccuracy:", accuracy_history[-1], "%")

    # visualize data
    if isVisualize:
        visualize_output(cost_history, accuracy_history, Weight, Bias, epochs, x_orig, y_orig)

    # save trained data to a file
    f = open(VAR.TRAINED_DATA_FILE, "w")
    for row in Weight:
        for col in range(Weight.shape[1]):
            f.write(str(row[col]) + " ")
        f.write("\n")

    f.write("|")    # separator
    for col in Bias:
        f.write(str(col) + " ")

    f.close()

    src = work_dir + "/" + VAR.TRAINED_DATA_FILE
    dst = VAR.GLOBAL_DIR + "/" + VAR.TRAINED_DATA_FILE
    # un-comment to copy the file to the mother (top-most) directory
    # copy_file(src, dst) # un-comment to copy the file

    end_time = datetime.now()
    print(str(end_time-start_time))
    return [Weight, Bias]


def copy_file(src, dst):
    try:
        copyfile(src, dst)
    except (SameFileError, IOError):
        print("Cannot copy the", VAR.TRAINED_DATA_FILE, "file")
        return VAR.ERROR_CODE


def visualize_dataset(x_orig, y_orig, original: bool = True):
    if original:
        # change back the dataset
        for row in x_orig:
            for col in range(len(row)):
                if col == 0:
                    row[col] = row[col] + VAR.SMOKE_OFFSET
                if col == 1:
                    row[col] = row[col] + VAR.TEMP_OFFSET

    # Positive Data Points
    x_pos = np.array([x_orig[i] for i in range(len(x_orig))
                      if y_orig[i] == 1])

    # Negative Data Points
    x_neg = np.array([x_orig[i] for i in range(len(x_orig))
                      if y_orig[i] == 0])

    # Plotting the Positive Data Points
    plt.scatter(x_pos[:, 0], x_pos[:, 1], color='blue', label='Fire')

    # Plotting the Negative Data Points
    plt.scatter(x_neg[:, 0], x_neg[:, 1], color='red', label='Safe')

    plt.xlabel('Smoke (ppm)')
    plt.ylabel('Temperature (°C)')
    plt.title('Plot of the dataset')
    plt.legend()

    plt.show()


def visualize_output(cost_history, accuracy_history, Weight, Bias, epochs, x_orig, y_orig):
    # visualize cost function
    plt.plot(list(range(epochs)), cost_history)
    plt.xlabel('Epochs')
    plt.ylabel('Cost')
    plt.title('Decrease in Cost with Epochs')
    plt.show()

    plt.plot(list(range(epochs)), accuracy_history)
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Increase in Accuracy with Epochs')
    plt.show()

    # Decision Boundary
    decision_boundary_x = np.array([np.min(x_orig[:, 0]),
                                    np.max(x_orig[:, 0])])

    decision_boundary_y = (- 1.0 / Weight[0]) * (decision_boundary_x * Weight + Bias)

    decision_boundary_y = [sum(decision_boundary_y[:, 0]),
                           sum(decision_boundary_y[:, 1])]

    # Positive Data Points
    x_pos = np.array([x_orig[i] for i in range(len(x_orig)) if y_orig[i] == 1])

    # Negative Data Points
    x_neg = np.array([x_orig[i] for i in range(len(x_orig)) if y_orig[i] == 0])

    # Plotting the Positive Data Points
    plt.scatter(x_pos[:, 0], x_pos[:, 1], color='blue', label='Positive')

    # Plotting the Negative Data Points
    plt.scatter(x_neg[:, 0], x_neg[:, 1], color='red', label='Negative')

    # Plotting the Decision Boundary
    plt.plot(decision_boundary_x, decision_boundary_y)
    plt.xlabel('Temp')
    plt.ylabel('Smoke')
    plt.title('Plot of Decision Boundary')

    plt.legend()

    axes = plt.gca()
    # axes.set_xlim([0, 250])
    # axes.set_ylim([20, 140])

    plt.show()
    plt.clf()


# train(True)
