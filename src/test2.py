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
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pprint
import ssl

if __name__ == '__main__':
    sia = SentimentIntensityAnalyzer
    date_sentiments = {}

    for i in range(1, 11):
        url = 'https://www.businesstimes.com.sg/search/facebook?page=' + str(i)
        context = ssl._create_unverified_context()
        page = urlopen(url, context=context).read()
        soup = BeautifulSoup(page, features="html.parser")
        posts = soup.findAll("div", {"class": "media-body"})
        for post in posts:
            time.sleep(1)
            url = post.a['href']
            date = post.time.text
            print(date, url)
            try:
                link_page = urlopen(url).read()
            except:
                url = url[:-2]
                link_page = urlopen(url).read()
            link_soup = BeautifulSoup(link_page)
            sentences = link_soup.findAll("p")
            passage = ""
            for sentence in sentences:
                passage += sentence.text
            sentiment = sia.polarity_scores(passage)['compound']
            date_sentiments.setdefault(date, []).append(sentiment)

    date_sentiment = {}

    for k, v in date_sentiments.items():
        date_sentiment[datetime.strptime(k, '%d %b %Y').date() + timedelta(days=1)] = round(sum(v) / float(len(v)), 3)

    earliest_date = min(date_sentiment.keys())

    print(date_sentiment)