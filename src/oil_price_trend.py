#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 2020

@author: Aditya Kalyan Jayanti
"""

import matplotlib.pyplot as plt
import pandas as pd

from src.oil_price_trend_specific import oil_price_trend_2012_2016


def read_data(data="Data/Cushing_OK_WTI_Spot_Price_FOB.csv"):
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
    data.columns = ['Date', 'OilPrice']

    # converting column to type date
    data['Date'] = pd.to_datetime(data.Date)

    trend_data = data

    # sorting values
    data = data.sort_values('Date')

    # The first 5 rows of the data frame
    # print(data.head())
    # initialize index to date column
    data.set_index('Date', inplace=True)
    # data = data.loc[datetime(1986, 2, 1):]

    # re-sampling with average monthly frequency
    # method of re-sampling = mean
    y = data['OilPrice'].resample('M').mean()
    y.plot(label="test", figsize=(20, 10), color='red')
    plt.ylabel("Oil Price Per Barrel in $USD", size=15)
    plt.xlabel("Year", size=15)
    plt.title("Average monthly frequency from (1986-2020)", size=25)
    plt.savefig('Results/AverageMonthlyFrequency.png',  bbox_inches='tight')
    # oil_prediction_lstm(data)
    oil_price_trend_2012_2016(trend_data)
