#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 2020

Updated on Sun Apr 5 2020

@author: Aditya Kalyan Jayanti
"""

import json
import re
from collections import OrderedDict

import matplotlib.pyplot as plt
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from numpy import log
from scipy.stats import spearmanr
from statsmodels.tsa.stattools import adfuller
from wordcloud import WordCloud, STOPWORDS


def eliminate_url(input1):
    input_text = input1.encode('ascii', 'ignore').decode('ascii')
    input_text = re.sub(r'http\S+', '', input_text)
    return input_text


def news_article_sentiment(data_oil, path="ScrapedNewsArticles/oil_news.json"):
    sia = SentimentIntensityAnalyzer()
    sentiment_value = {}
    with open(path) as news_file:
        data = json.load(news_file, encoding='utf-8')

    reversed_data = OrderedDict()

    stack = []
    for k, v in data.items():
        stack.append((k, v))

    stack = list(reversed(stack))

    for article in stack:
        reversed_data[article[0]] = article[1]

    # storing value in a variable to be processed in word cloud function
    data_frame_word_cloud = data

    for key in data:
        sentiment = sia.polarity_scores(data[key])['compound']
        sentiment_value[key] = sentiment

    df = pd.DataFrame(sentiment_value.items(), columns=['date', 'sentiment'])

    df['date'] = pd.to_datetime(df['date'])

    df['year'] = df['date'].dt.year

    df = df.groupby('year').mean().reset_index()

    ax = plt.subplot(211)
    ax.plot(df.year, df['sentiment'],  color='r')
    ax.set_xticks([2012, 2013, 2014, 2015, 2016])
    plt.ylabel("Magnitude of sentiment values")
    plt.xlabel("Year")
    plt.title("Trend of News Sentiment (2012-2016)")
    plt.savefig('Results/SentimentOfCrudeOilNews.png', bbox_inches='tight')

    # Augmented Dickey-Fuller Test
    # Statistical test for checking if a time series is stationary
    print("Augmented Dickey-Fuller Test")
    dickey_fuller_test = df['sentiment'].to_numpy()
    dickey_fuller_test = log(dickey_fuller_test)
    result = adfuller(dickey_fuller_test)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))

    # df.set_index('date', inplace=True)
    #
    # print(df.head())
    #
    # # resampling the data with a rolling mean
    # df.rolling('6H').mean().plot()
    # plt.show()

    # CORRELATION
    print("-----------------CORRELATION--------------")
    data_oil['Date'] = pd.to_datetime(data_oil['Date'])
    data_oil['year'] = data_oil['Date'].dt.year
    data_oil = data_oil.groupby('year').mean().reset_index()
    range_dates = (data_oil['year'] > 2011) & (data_oil['year'] <= 2016)
    data_oil = data_oil.loc[range_dates]
    print(data_oil.head())
    print(df)
    corr = data_oil['OilPrice'].corr(df['sentiment'], method="kendall")
    print("CORR = ", corr)
    print("-----------------CORRELATION--------------")

    # function call to word cloud generator
    word_cloud_generator(data_frame_word_cloud)


def word_cloud_generator(data_frame):
    data_frame = pd.DataFrame(data_frame.items(), columns=['date', 'article'])
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    year_2016 = data_frame[data_frame.date.dt.year.eq(2016)]
    text = ""
    for article in year_2016['article']:
        text += eliminate_url(article)
    show_word_cloud(text)


def show_word_cloud(data):
    """
    program to generate a word cloud
    :param data: collection of reviews
    :return:
    """
    stopwords = STOPWORDS
    word_cloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40,
        scale=3,
        random_state=1
    ).generate(str(data))
    plt.axis('off')
    plt.imshow(word_cloud)
    plt.show()


