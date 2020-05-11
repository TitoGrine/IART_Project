from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.models import Sequential
from sklearn.base import BaseEstimator


class CNN(BaseEstimator):
    def __init__(self, dropout_rate=0.2, filters=250,
                 kernel_size=3, units=250, activation_conv='relu',
                 activation_end='sigmoid', loss_function='binary_crossentropy'):
        self.loss_function = loss_function
        self.activation_end = activation_end
        self.activation_conv = activation_conv
        self.units = units
        self.kernel_size = kernel_size
        self.filters = filters
        self.dropout_rate = dropout_rate

    def fit(self, x, y=None):
        model = Sequential()
        model.add(Embedding(len(x), 50))
        model.add(Dropout(self.dropout_rate))

        model.add(Conv1D(self.filters, self.kernel_size, activation=self.activation_conv))

        model.add(GlobalMaxPooling1D())

        model.add(Dense(self.units))

        model.add(Dense(7))
        model.add(Activation(self.activation_end))

        model.compile(loss=self.loss_function, optimizer='accuracy')
        model.fit(x, y, batch_size=32, epochs=3)