import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

bankdata = pd.read_csv("E:/Thesis/iFASTATHANU-Flask-Python/AI/Dataset/bill_authentication.csv")

X = bankdata.drop('Class', axis=1)
y = bankdata['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(confusion_matrix(y_test, y_pred))
ax.grid(False)
ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
ax.set_ylim(1.5, -0.5)
for i in range(2):
    for j in range(2):
        ax.text(j, i, confusion_matrix(y_test, y_pred)[i, j], ha='center', va='center', color='red')
plt.show()




