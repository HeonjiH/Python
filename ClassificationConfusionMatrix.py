import seaborn as sn
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report

y_true = ["cat", "ant", "cat", "cat", "ant", "bird"]
y_pred = ["and", "ant", "ant", "cat", "ant", "bird"]
labels = ["ant", "cat", "bird"]

# create matrix
cm = confusion_matrix(y_true, y_pred, labels=labels)


# visualize the confusion matrix
df_cm = pd.DataFrame(cm, labels, labels)
ax = sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, square=True, cbar=False, fmt='g')
ax.set_ylim(0, 3) #this manually corrects the cutoff issue in sns.heatmap found in matplotlib ver 3.1.1
plt.xlabel("Predicted")
plt.ylabel("Actual")
ax.invert_yaxis() #optional
# plt.show()

# calcuation f1 score
micro_precision = precision_score(y_true, y_pred, average="micro")
micro_recall = recall_score(y_true, y_pred, average="micro")
micro_f1_score = f1_score(y_true, y_pred, average="micro")

print("Micro Precision {:.2f}".format(micro_precision))
print("Micro Recall {:.2f}".format(micro_recall))
print("Micro F1-score {:.2f}".format(micro_f1_score))

# Calculates the F1 score for each class
print("\nClassification Report\n")
print(classification_report(y_true, y_pred))


class ExcelHelper:
    def __init__(self, path="", fileName=""):
        self._fileName = fileName
        self._path = path
        self.dataset = pd.read_excel(f"{path}/{fileName}", index_col=0)
    
    def classifyData(self, key):
        filterData = self.dataset[self.dataset["구분"] == key][["질문", "답변"]]
        return filterData