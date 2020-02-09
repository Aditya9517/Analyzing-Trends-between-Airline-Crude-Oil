import seaborn as sea
import matplotlib.pyplot as plt
from fbprophet import Prophet
import pandas as pd


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


def prediction(data):
    pd.plotting.register_matplotlib_converters()
    fb_forecasting = Prophet()
    data_frame = data

    # Prophet follows sklearn API
    # The input to Prophet is always a date frame with two columns 'ds' and 'y'
    # reference: https://facebook.github.io/prophet/
    data_frame.columns = ['ds', 'y']

    fb_forecasting.fit(data_frame)

    future = fb_forecasting.make_future_dataframe(periods=90)

    forecast = fb_forecasting.predict(future)
    fb_forecasting.plot_components(forecast)
    plt.savefig('Results/trend.png', bbox_inches='tight')
    plt.show()
    fb_forecasting.plot(forecast)
    plt.savefig('Results/forecast.png', bbox_inches='tight')
    plt.show()








