#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 2020

@author: Aditya Kalyan Jayanti
"""

import pandas as pd


def read_combined_data(file_path="../Data/AirlineData/combined_2016.csv"):
    """
    reads the combined 2016 flight data using pandas
    :param file_path: contains 2016 airline performance data
    :return: pandas data frame
    """
    # the data frame contains 5617658 rows and 43 columns
    df = pd.read_csv(file_path, low_memory=False)

    print("(Rows,Columns) = ", df.shape)

    # to analyze missing values and information about the data
    information = pd.DataFrame(df.dtypes).T.rename(index={0: 'Data Type'})
    information = information.append(pd.DataFrame(df.isnull().sum())).T.rename(index={0: 'Null Values'})
    information = information.append(pd.DataFrame(df.isnull().sum() / df.shape[0] * 100).T.rename(index={0: 'Percentage '
                                                                                                            'Of Null '
                                                                                                            'Values'}))
    print(information)


if __name__ == '__main__':
    read_combined_data()
