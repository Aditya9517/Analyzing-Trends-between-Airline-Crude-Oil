#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 2020

@author: Aditya Kalyan Jayanti
"""


import seaborn as sea
import matplotlib.pyplot as plt
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric
from fbprophet.plot import add_changepoints_to_plot
import pandas as pd
import copy
import math
import sklearn.metrics as metrics


def oil_price_trend_2012_2016(data):
    """
    Function filters data frame for specific dates between 2012 and 2016
    :param data:
    :return:
    """
    start_date = '2012-01-01'
    end_date = '2016-12-31'
    range_dates = (data['Date'] > start_date) & (data['Date'] <= end_date)
    date_frame = data.loc[range_dates]
    plt.figure(figsize=(10, 5))
    sea.lineplot(x='Date', y='OilPrice', data=date_frame, color='k')
    plt.title("WTI Crude Oil Price Trend")
    plt.show()
    prediction(data)
    return data


def prediction(data):
    pd.plotting.register_matplotlib_converters()
    fb_forecasting = Prophet(n_changepoints=4)
    data_frame = copy.deepcopy(data)


    # Prophet follows sklearn API
    # The input to Prophet is always a date frame with two columns 'ds' and 'y'
    # reference: https://facebook.github.io/prophet/
    data_frame.columns = ['ds', 'y']
    data_frame['y'].replace('  ', '', inplace=True)
    data_frame.dropna(subset=['y'], inplace=True)
    fb_forecasting.fit(data_frame)
    future = fb_forecasting.make_future_dataframe(periods=250)
    forecast = fb_forecasting.predict(future)
    fb_forecasting.plot_components(forecast)
    plt.title("Trend analysis of crude oil prices")
    plt.savefig('Results/trend.png', bbox_inches='tight')
    plt.show()
    print("------------FORECAST----------------")
    forecast.to_csv('forecast.csv', index=False)
    print("------------FORECAST----------------")
    fig = fb_forecasting.plot(forecast, xlabel="Year", ylabel="Crude Oil Price")
    a = add_changepoints_to_plot(fig.gca(), fb_forecasting, forecast)
    plt.title("Prophet Forecasting Model")
    plt.savefig('Results/forecast.png', bbox_inches='tight')
    plt.show()

    # Prophet Oil Forecasts
    forecast2019 = forecast[(forecast['ds'] >= '2019-01-01') & (forecast['ds'] <= '2020-01-21')]
    figure, ax = plt.subplots()
    ax.plot(forecast2019['ds'], forecast2019['yhat'], label='Predicted Crude Oil Prices', color="red")
    prophet_data = data[data['Date'] >= '2019-01-01']
    ax.plot(prophet_data['Date'], prophet_data['OilPrice'], label='Original Crude Oil Prices', color="orange")
    plt.ylim([0, 90])
    legend = ax.legend(loc='upper right', shadow=True)
    plt.title('Crude Oil Prices Forecasting using Prophet')
    plt.xlabel('Months')
    plt.ylabel('Crude Oil Prices')
    plt.savefig('Results/ForecastUsingProphet.png', bbox_inches='tight')
    plt.show()

    # Mean Absolute Error
    mean_abs_error = metrics.mean_absolute_error(prophet_data['OilPrice'], forecast2019['yhat'])

    # Mean Squared Error
    mean_square_error = metrics.mean_squared_error(prophet_data['OilPrice'], forecast2019['yhat'])

    # Root Mean Squared Error
    root_mean_square_error = math.sqrt(mean_square_error)

    print("Mean Absolute Error = ", mean_abs_error)
    print("Mean Squared Error = ", mean_square_error)
    print("Root Mean Squared Error = ", root_mean_square_error)

    # Prophet Diagnostics

    cross_validation_forecast = cross_validation(fb_forecasting, initial='1259 days', period='180 days',
                                                 horizon='365 days')

    cutoff = cross_validation_forecast['cutoff'].unique()[0]

    cross_validation_forecast = cross_validation_forecast[cross_validation_forecast['cutoff'].values == cutoff]

    performance = performance_metrics(cross_validation_forecast)

    print(performance.head())

    plot_cross_validation_metric(cross_validation_forecast, metric='mape')
    plt.title("Cross Validation Performance Metrics")
    plt.savefig('Results/ProphetDiagnostics.png', bbox_inches='tight')
    plt.show()


