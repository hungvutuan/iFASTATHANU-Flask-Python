import sys
import matplotlib.pyplot as plt
from AI import logit_reg_2 as r
import tensorflow as tf
import numpy as np

init = tf.compat.v1.global_variables_initializer()
weight = r.val[0]
bias = r.val[1]

x_orig = r.x_orig
x = np.array(np.zeros(weight.shape))
prediction = np.array(np.zeros(weight.shape[0]))
holder = 0


def __calc(val):
    count = [0, 0]
    for row in range(weight.shape[0]):
        count[0] = count[0] + val[0] * weight[row][0]
        count[1] = count[1] + val[1] * weight[row][1]

    return count[0] + count[1]


def calc(val):
    # total = np.dot(weight[-1], val) + bias
    total = r.sigmoid(val[0] * weight[-1][0] + bias[0]) + \
            r.sigmoid(val[1] * weight[-1][1] + bias[1])
    return total


for i in range(x.shape[0]):
    for k in range(x.shape[1]):
        x[i][k] = r.sigmoid(x_orig[i][k] * weight[i][k] + bias[k])

    prediction[i] = r.sigmoid(x[i][0] + x[i][1])

fire_val = [-27, -5]
for i in range(len(weight)):
    holder = holder + \
             r.sigmoid(
                 r.sigmoid(fire_val[0] * weight[i][0] + bias[0]) +
                 r.sigmoid(fire_val[1] * weight[i][1] + bias[1])
             )

# print(fire_val[0]*)
prediction = np.reshape(prediction, (len(prediction), -1))

# plt.plot(x_orig[:prediction.shape[0]], r.sigmoid(x_orig[:prediction.shape[0]]))
plt.plot(x_orig[:prediction.shape[0]], x)
plt.title("Sigmoid for accuracy")
# plt.legend()
plt.show()

_calc = calc(fire_val)
print("Result: ", _calc * 100)

# a = r.sigmoid(fire_val[0]+)
Y_hat = tf.nn.sigmoid(tf.add(tf.matmul(np.transpose(weight), fire_val), bias))
with tf.compat.v1.Session() as sess:
    sess.run(init)
    y_hat = sess.run(Y_hat)
    print(y_hat)

print("Done")

