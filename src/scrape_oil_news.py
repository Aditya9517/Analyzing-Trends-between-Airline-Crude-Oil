import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import csv
from newspaper import Article
from datetime import datetime
import json
import Algorithmia
import nltk
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def main():
    sia = SentimentIntensityAnalyzer()
    f = "%m-%Y-%dT%H:%M:%S.%fZ"
    URL = "https://www.upi.com/search/?s_l=articles&ss=%22oil+market%22&offset="
    sentiment_analysis = {}
    soup = BeautifulSoup(requests.get("https://oilprice.com/Latest-Energy-News/World-News/Page-1060.html").content, features="lxml")
    main_div = soup.select_one("div.tableGrid__column.tableGrid__column--articleContent.category")

    divs = main_div.select('div.categoryArticle__content')

    links = [(d.select_one("p.categoryArticle__meta").text.split("|")[0].strip(), d.a["href"]) for d in divs]
    date = links[0][0]
    date = date.replace("at", "")
    date = date.replace(",", "")

    datetime_object = datetime.strptime(date, '%b %d %Y %H:%M')

    for i in range(len(links)):
        article = Article(links[i][1])
        date = links[i][0]
        date = date.replace("at", "")
        date = date.replace(",", "")
        datetime_object = datetime.strptime(date, '%b %d %Y %H:%M')
        article.download()
        article.parse()
        # print(datetime_object)
        sentiment = sia.polarity_scores(article.text)['compound']
        # print(sentiment)
        sentiment_analysis[datetime_object] = sentiment

    x = list(sentiment_analysis.keys())
    y = list(sentiment_analysis.values())
    plt.plot(x, y)
    plt.show()



    # with open('test.csv', 'w') as f:
    #     for key in sentiment.keys():
    #         f.write("%s, %s\n" % (key, sentiment[key]))


if __name__ == '__main__':
    main()
