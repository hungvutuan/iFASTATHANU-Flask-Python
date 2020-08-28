import pandas as pd
import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt

import seaborn as sns
sns.set(style="darkgrid")

cols = ['price', 'maint', 'doors', 'persons', 'lug_capacity', 'safety','output']
cars = pd.read_csv(r'/content/drive/My Drive/datasets/car_dataset.csv', names=cols, header=None)

