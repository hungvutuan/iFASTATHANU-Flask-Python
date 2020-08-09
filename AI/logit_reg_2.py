# import pathlib
#
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import seaborn as sns
#
# import tensorflow as tf
#
# from tensorflow import keras
# from tensorflow.keras import layers
#
# # import tensorflow_docs as tfdocs
# # import tensorflow_docs.plots
# # import tensorflow_docs.modeling
#
# # Download dataset
# dataset_path = keras.utils.get_file("auto-mpg.data", "http://archive.ics.uci.edu/ml/machine-learning-databases/auto"
#                                                      "-mpg/auto-mpg.data")
#
# # Set name for columns
# column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight',
#                 'Acceleration', 'Model Year', 'Origin']
#
# # load dataset to a variable
# dataset = pd.read_csv(dataset_path, names=column_names,
#                       na_values="?", comment='\t',
#                       sep=" ", skipinitialspace=True)
#
# dataset.tail()
#
# # Check for na (Not available) values
# # dataset.isna().sum()
#
# # Drop N.A. rows
# dataset = dataset.dropna()
#
# # The "Origin" column is really categorical, not numeric. So convert that to a one-hot:
# dataset['Origin'] = dataset['Origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
# # for row in dataset['Origin']:
# #     print(row)

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Step 2: Get data
x = np.arange(10).reshape(-1, 1)
y = np.array([0, 1, 0, 0, 1, 1, 1, 1, 1, 1])






































