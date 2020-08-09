import tensorflow as tf
import numpy as np

# mnist = tf.keras.datasets.mnist
#
# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0
#
# print(x_train, x_test)
#
# model = tf.keras.models.Sequential([
#   tf.keras.layers.Flatten(input_shape=(28, 28)),
#   tf.keras.layers.Dense(128, activation='relu'),
#   tf.keras.layers.Dropout(0.2),
#   tf.keras.layers.Dense(10)
# ])
# # print("model:", model)
#
# predictions = model(x_train[:1]).numpy()
# print("prediction:", predictions)
#
# tf.nn.softmax(predictions).numpy()
# print("prediction:", predictions)

# ---

# X = numpy.zeros([157, 128])  # a matrix of 157 x 128 dimension of 0's
# Y = numpy.zeros([157], dtype=numpy.int32)  # a vector of 157 0's
#
# example_id = numpy.array(['%d' % i for i in range(len(Y))])
# print(example_id, "\n", Y)
#
# train_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(
#     x={"X": X, "example_id": example_id},
#     y=Y,
#     num_epochs=None,
#     shuffle=True)
#
# svm = tf.compat.v1.contrib.learn.SVM(
#     example_id_column="example_id",
#     feature_columns=(tf.contrib.layers.real_valued_column(
#         column_name="X", dimension=128),),
#     l2_regularization=0.1)


import matplotlib.pyplot as plt
# import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

x = np.arange(10).reshape(-1, 1)
y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

model = LogisticRegression(solver='liblinear', C=10.0, random_state=0)
model.fit(x, y)

# evaluate the model
# model.predict_proba(x)
# model.predict(x)

cm = confusion_matrix(y, model.predict(x))

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(cm)
ax.grid(False)
ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
ax.set_ylim(1.5, -0.5)
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha='center', va='center', color='red')
plt.show()

# print report
print(classification_report(y, model.predict(x)))
