import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def build_comparison_graph(labels, values, values_labels, width):
    x = np.arange(len(labels))  # the label locations

    fig, ax = plt.subplots()
    rects = [ax.bar((x - width / 2) + width * i, value, width, label=values_labels[i]) for i, value in
             enumerate(values)]

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    fig.tight_layout()

    plt.show()


def get_scores(y_test, y_pred):
    f1 = f1_score(y_test, y_pred, average="macro")
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="macro")
    recall = recall_score(y_test, y_pred, average="macro")
    return [f1, acc, precision, recall]
