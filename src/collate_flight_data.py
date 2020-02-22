#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 2020

@author: Aditya Kalyan Jayanti
"""

# this file reads the on-time performance of Airlines
import pandas as pd


def read_on_time_data(months, file_path="../Data/AirlineData/"):

    # concatenating data for each month in the year of 2016
    combined_airline_data_2016 = pd.concat([pd.read_csv(file_path + "Airline" + f + "2016" + ".csv", low_memory=False)
                                            for f in months])

    # saving the combined data in to a csv
    combined_airline_data_2016.to_csv(file_path + "combined_2016.csv", index=False)


if __name__ == '__main__':

    # list containing name of the months in a year
    list_of_months = ["January", "February", "March", "April", "May", "June", "July",
                      "August", "September", "October", "November", "December"]

    # function call to read airline data
    read_on_time_data(list_of_months)
