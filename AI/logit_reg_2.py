# importing modules
import os

import numpy as np
import pandas as pd
import tensorflow as tf 
import matplotlib.pyplot as plt 
from sklearn.preprocessing import OneHotEncoder

work_dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
# data = pd.read_csv(work_dir+'/Dataset/dataset_iris.csv', header=None)
time_iter = 0.0454

tf.compat.v1.disable_eager_execution()

# Set dataset
fire = np.genfromtxt(work_dir + "/Dataset/fire.csv", delimiter=',', )
non_fire = np.genfromtxt(work_dir + "/Dataset/non-fire.csv", delimiter=',', )

# Feature Matrix
fire = np.delete(fire, 0, 1)
non_fire = np.delete(non_fire, 0, 1)
x_orig = np.append(fire, non_fire, 0)

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
x_pos = np.array([x_orig[i] for i in range(len(x_orig))
                  if y_orig[i] == 1])

# Negative Data Points
x_neg = np.array([x_orig[i] for i in range(len(x_orig))
                  if y_orig[i] == 0])

# # Plotting the Positive Data Points
# plt.scatter(x_pos[:, 0], x_pos[:, 1], color='blue', label='Positive')
#
# # Plotting the Negative Data Points
# plt.scatter(x_neg[:, 0], x_neg[:, 1], color='red', label='Negative')
#
# plt.xlabel('Feature 1')
# plt.ylabel('Feature 2')
# plt.title('Plot of given data')
# plt.legend()
#
# plt.clf()                     

# Creating the One Hot Encoder
oneHot = OneHotEncoder()

# Encoding x_orig
oneHot.fit(x_orig)
x = oneHot.transform(x_orig).toarray()

# Encoding y_orig
oneHot.fit(y_orig)
y = oneHot.transform(y_orig).toarray()

alpha, epochs = 0.5, 200
m, n = x.shape
print('m =', m)
print('n =', n)
print('Learning Rate =', alpha)
print('Number of Epochs =', epochs)

# There are n columns in the feature matrix
# after One Hot Encoding.
X = tf.compat.v1.placeholder(tf.float32, [None, n])

# Since this is a binary classification problem,
# Y can take only 2 values.
Y = tf.compat.v1.placeholder(tf.float32, [None, 2])

# Trainable Variable Weights
W = tf.Variable(tf.zeros([n, 2]))

# Trainable Variable Bias
b = tf.Variable(tf.zeros([2]))

# Hypothesis
Y_hat = tf.nn.sigmoid(tf.add(tf.matmul(X, W), b))

# Sigmoid Cross Entropy Cost Function
cost = tf.nn.sigmoid_cross_entropy_with_logits(
    logits=Y_hat, labels=Y)

# Gradient Descent Optimizer
optimizer = tf.compat.v1.train.GradientDescentOptimizer(
    learning_rate=alpha).minimize(cost)

# Global Variables Initializer
init = tf.compat.v1.global_variables_initializer()

# Starting the Tensorflow Session
with tf.compat.v1.Session() as sess:
    # Initializing the Variables
    sess.run(init)

    # Lists for storing the changing Cost and Accuracy in every Epoch
    cost_history, accuracy_history = [], []

    # Iterating through all the epochs
    for epoch in range(epochs):
        cost_per_epoch = 0
        # Running the Optimizer
        sess.run(optimizer, feed_dict={X: x, Y: y})

        # Calculating cost on current Epoch
        c = sess.run(cost, feed_dict={X: x, Y: y})

        # Calculating accuracy on current Epoch
        correct_prediction = tf.equal(tf.argmax(Y_hat, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        # Storing Cost and Accuracy to the history
        cost_history.append(sum(sum(c)))
        accuracy_history.append(accuracy.eval({X: x, Y: y}) * 100)

        # Displaying result on current Epoch
        if epoch % 100 == 0 and epoch != 0:
            print("Epoch " + str(epoch) + " Cost: "
                  + str(cost_history[-1]))

    Weight = sess.run(W)  # Optimized Weight
    Bias = sess.run(b)  # Optimized Bias

    # Final Accuracy
    correct_prediction = tf.equal(tf.argmax(Y_hat, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print("\nAccuracy:", accuracy_history[-1], "%")

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

# Calculating the Decision Boundary
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
