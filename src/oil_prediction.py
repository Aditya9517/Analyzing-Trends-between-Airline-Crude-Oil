import datetime
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from keras.callbacks import ReduceLROnPlateau

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout, Dense

warnings.filterwarnings("ignore")


def read_data(data):
    """
    reads the data from CSV file, renames column names, plots the
    average monthly frequency of historical oil prices from 1987
    to 2020, and calls oil prediction method.
    :param data: Historical WTI Crude oil prices as a CSV file
    :return: None
    """
    flag = 0
    with open(data, 'r') as file:
        while flag < 4:
            next(file)
            flag += 1
        data = pd.read_csv(file, sep=',')

    # renaming column names
    data.columns = ['date', 'price']

    # converting column to type date
    data['date'] = pd.to_datetime(data.date)
    print(data.head())

    # sorting values
    data = data.sort_values('date')

    # initialize index to date column
    data.set_index('date', inplace=True)
    data = data.loc[datetime.date(year=1986, month=2, day=1):]

    # re-sampling with average monthly frequency
    # method of re-sampling = mean
    y = data['price'].resample('M').mean()
    y.plot(label="test", figsize=(20, 10), color='red')
    plt.ylabel("Oil Price Per Barrel in $USD", size=15)
    plt.xlabel("Year", size=15)
    plt.title("Average monthly frequency from (1986-2020)", size=25)
    plt.show()
    oil_prediction_lstm(data)


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
    x_train_data = []
    y_train_data = []
    x_test_data = []
    y_test_data = []
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

    h = regressor.fit(xy_train_test[0], xy_train_test[1], epochs=20, batch_size=15,
                      validation_data=(xy_train_test[2], xy_train_test[3]),
                      callbacks=[reduce_learning_rate], shuffle=False)

    predict_train_data = regressor.predict(xy_train_test[0])
    predict_test_data = regressor.predict(xy_train_test[2])

    predict_train_data = scaler.inverse_transform(predict_train_data)
    xy_train_test[1] = scaler.inverse_transform([xy_train_test[1]])
    predict_test_data = scaler.inverse_transform(predict_test_data)
    xy_train_test[3] = scaler.inverse_transform([xy_train_test[3]])

    x = [i for i in range(360)]
    plt.plot(x, xy_train_test[3][0][:360], marker='.', label='actual')
    plt.plot(x, predict_test_data[:, 0][:360], 'r', label='production')
    plt.show()
    plt.tight_layout()
