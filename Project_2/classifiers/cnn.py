from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.models import Sequential
from sklearn.base import BaseEstimator
import numpy as np


class CNN(BaseEstimator):
    def __init__(self, dropout_rate=0.2, filters=250,
                 kernel_size=3, units=250, activation_conv='relu',
                 activation_end='sigmoid', loss_function='sparse_categorical_crossentropy', epochs=3):
        self.epochs = epochs
        self.loss_function = loss_function
        self.activation_end = activation_end
        self.activation_conv = activation_conv
        self.units = units
        self.kernel_size = kernel_size
        self.filters = filters
        self.dropout_rate = dropout_rate
        self.model = Sequential()

    def fit(self, x, y):
        self.model.add(Embedding(x.size, 50))
        self.model.add(Dropout(self.dropout_rate))

        self.model.add(Conv1D(self.filters, self.kernel_size, activation=self.activation_conv))

        self.model.add(GlobalMaxPooling1D())

        self.model.add(Dense(self.units))

        self.model.add(Dense(3))
        self.model.add(Activation(self.activation_end))

        self.model.compile(loss=self.loss_function, optimizer='adam')
        self.model.fit(x, y, batch_size=32, epochs=self.epochs)
        return self.model

    def predict(self, x_test):
        return np.argmax(self.model.predict(x_test, batch_size=64, verbose=1), axis=1)
