#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 2020

@author: Aditya Kalyan Jayanti
"""
from collections import OrderedDict

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def read_combined_data(file_path="../Data/AirlineData/AirlineFebruary2016.csv"):
    """
    reads the combined 2016 flight data using pandas
    :param file_path: contains 2016 airline performance data
    :return: pandas data frame
    """
    # the data frame contains 5617658 rows and 43 columns
    df = pd.read_csv(file_path, low_memory=False)

    print("(Rows,Columns) = ", df.shape)

    # remove attributes containing > 90% missing values
    attributes_removed = ['CANCELLATION_CODE', 'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY',
                          'LATE_AIRCRAFT_DELAY', 'FIRST_DEP_TIME']

    df.drop(attributes_removed, axis=1, inplace=True)

    # to analyze missing values and information about the data
    missing_values = df.isnull().sum(axis=0).reset_index()
    missing_values.columns = ['Attribute Name', 'Missing Values']
    missing_values['Percentage'] = (df.shape[0] - missing_values['Missing Values']) / df.shape[0] * 100
    missing_values.sort_values('Percentage').reset_index(drop=True)

    print(missing_values)
    IATA_airports = pd.read_csv("../Data/airport_IATA.csv")

    number_of_flights = df['ORIGIN'].value_counts()

    plt.figure(figsize=(11, 11))
    colors = ['yellow', 'red', 'lightblue', 'purple', 'green', 'orange']
    size_limits = [1, 100, 1000, 10000, 100000, 1000000]
    labels = []

    for i in range(len(size_limits) - 1):
        labels.append("{} <.< {}".format(size_limits[i], size_limits[i + 1]))

    world_map = Basemap(resolution='i', llcrnrlon=-180, urcrnrlon=-50,
                  llcrnrlat=10, urcrnrlat=75, lat_0=0, lon_0=0, )
    world_map.shadedrelief()
    world_map.drawcoastlines()
    world_map.drawcountries(linewidth=3)
    world_map.drawstates(color='0.3')

    for index, (code, y, x) in IATA_airports[['IATA_CODE', 'LATITUDE', 'LONGITUDE']].iterrows():
        x, y = world_map(x, y)
        count_number_of_flights_per_region = 0
        if code not in number_of_flights:
            count_number_of_flights_per_region = 0
        else:
            count_number_of_flights_per_region = int(number_of_flights[code])

        isize = [i for i, val in enumerate(size_limits) if val < count_number_of_flights_per_region]

        if isize:
            ind = isize[-1]
        else:
            ind = 0
        world_map.plot(x, y, marker='o', markersize=ind + 5, markeredgewidth=1, color=colors[ind],
                 markeredgecolor='k', label=labels[ind])

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    print(by_label)
    key_order = ('1 <.< 100', '100 <.< 1000', '1000 <.< 10000',
                 '10000 <.< 100000')
    # key_order = ('1 <.< 100', '100 <.< 1000', '1000 <.< 10000',
    #              '10000 <.< 100000', '100000 <.< 1000000')
    new_label = OrderedDict()
    for key in key_order:
        new_label[key] = by_label[key]
    plt.legend(new_label.values(), new_label.keys(), loc=1, prop={'size': 11},
               title='Number of flights per year', frameon=True, framealpha=1)
    plt.savefig('../Results/AirlineOrigin.png', bbox_inches='tight')


if __name__ == '__main__':
    read_combined_data()
