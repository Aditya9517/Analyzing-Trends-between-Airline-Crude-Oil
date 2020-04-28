#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 4 2020

@author: Aditya Kalyan Jayanti
"""

import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import ReduceLROnPlateau
from keras.layers import Dropout, Dense
from keras.layers import LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


def convert_array_dataset(dataset, val):
    """

    :param dataset:
    :param val:
    :return:
    """
    x = []
    y = []
    for i in range(len(dataset)-val-1):
        z = dataset[i:(i+val), 0]
        x.append(z)
        y.append(dataset[i+val, 0])
    return np.array(x), np.array(y)


def split_into_train_test(wti_data):
    """

    :param wti_data:
    :return:
    """
    print("Splitting data in to train/test 70:30")

    # normalizing the dataset to [0,1]
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = scaler.fit_transform(wti_data)

    # creating train and test data
    train = int(len(data) * 0.70)
    test = len(data) - train
    train, test = data[0:train, :], data[train:len(data), :]

    return train, test, scaler


def reshape_data(train_data, test_data):
    """

    :param train_data:
    :param test_data:
    :return:
    """
    x_train_data, y_train_data = convert_array_dataset(train_data, 90)
    x_train_data = np.reshape(x_train_data, (x_train_data.shape[0], x_train_data.shape[1], 1))
    x_test_data, y_test_data = convert_array_dataset(test_data, 90)
    x_test_data = np.reshape(x_test_data, (x_test_data.shape[0], x_test_data.shape[1], 1))

    return [x_train_data, y_train_data, x_test_data, y_test_data]


def oil_prediction_lstm(wti_data):
    """
    Method to forecast oil prices using historical oil price data,
    (determining crude oil prices using internal factors)
    :param wti_data: Historical WTI Crude oil prices
    :return:
    """
    train, test, scaler = split_into_train_test(wti_data)
    xy_train_test = reshape_data(train, test)
    regressor = Sequential()
    regressor.add(LSTM(units=60, return_sequences=True, input_shape=(xy_train_test[0].shape[1], 1)))
    regressor.add(Dropout(0.1))
    regressor.add(LSTM(units=60, return_sequences=True))
    regressor.add(Dropout(0.1))
    regressor.add(LSTM(units=60))
    regressor.add(Dropout(0.1))
    regressor.add(Dense(units=1))
    regressor.compile(optimizer='adam', loss='mean_squared_error')

    # Reduce learning rate if no improvement is observed
    reduce_learning_rate = ReduceLROnPlateau(monitor='val_loss', patience=5)

    h = regressor.fit(xy_train_test[0], xy_train_test[1], epochs=5, batch_size=15,
                      validation_data=(xy_train_test[2], xy_train_test[3]),
                      callbacks=[reduce_learning_rate], shuffle=False)

    predict_train_data = regressor.predict(xy_train_test[0])
    predict_test_data = regressor.predict(xy_train_test[2])

    predict_train_data = scaler.inverse_transform(predict_train_data)
    xy_train_test[1] = scaler.inverse_transform([xy_train_test[1]])
    predict_test_data = scaler.inverse_transform(predict_test_data)
    xy_train_test[3] = scaler.inverse_transform([xy_train_test[3]])

    x = [i for i in range(180)]
    plt.plot(x, xy_train_test[3][0][:180], marker='.', label='actual')
    plt.plot(x, predict_test_data[:, 0][:180], 'r', label='production')
    plt.show()
    plt.tight_layout()

    train_predict = regressor.predict(xy_train_test[0])
    test_predict = regressor.predict(xy_train_test[2])

    # invert predictions
    train_predict = scaler.inverse_transform(train_predict)
    Y_train = scaler.inverse_transform([xy_train_test[1]])
    test_predict = scaler.inverse_transform(test_predict)
    Y_test = scaler.inverse_transform([xy_train_test[3]])

    print("-------------------------------------------PREDICTION ERRORS -------------------------------------------")

    print('Train Mean Absolute Error:', mean_absolute_error(Y_train[0], train_predict[:, 0]))
    print('Train Root Mean Squared Error:', np.sqrt(mean_squared_error(Y_train[0], train_predict[:, 0])))
    print('Test Mean Absolute Error:', mean_absolute_error(Y_test[0], test_predict[:, 0]))
    print('Test Root Mean Squared Error:', np.sqrt(mean_squared_error(Y_test[0], test_predict[:, 0])))
    print("-------------------------------------------PREDICTION ERRORS -------------------------------------------")
