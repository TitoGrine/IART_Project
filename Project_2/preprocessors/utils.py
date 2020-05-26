from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import time


def oversample_data(x, y):
    oversampler = SMOTE()
    return oversampler.fit_resample(x, y)


def split(x, y, oversample=False):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    if oversample:
        x_train, y_train = oversample_data(x_train, y_train)

    x_over, y_over = oversample_data(x_train, y_train)
    return x_over, y_over, x_test, y_test


def fit(x, y, clsf, oversample=False):
    x_over, y_over, x_test, y_test = split(x, y, oversample=oversample)
    start = time.time()
    clsf.fit(x_over, y_over)
    y_pred = clsf.predict(x_test)
    print(classification_report(y_test, y_pred, zero_division=0))
    return y_test, y_pred, (time.time() - start)
