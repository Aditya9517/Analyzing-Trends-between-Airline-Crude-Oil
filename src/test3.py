from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from collections import OrderedDict

if __name__ == '__main__':
    path = "../ScrapedNewsArticles/oil_news.json"
    sia = SentimentIntensityAnalyzer()
    develop = {}
    sentiment_value = {}
    with open(path) as news_file:
        data = json.load(news_file, encoding='utf-8')

    reversed_data = OrderedDict()
    for k in reversed(data):
        reversed_data[k] = data[k]

    data = reversed_data

    # storing value in a variable to be processed in word cloud function
    data_frame_word_cloud = data

    for key in data:
        sentiment = sia.polarity_scores(data[key])['compound']
        sentiment_value[key] = sentiment
        develop[sentiment] = data[key]

    with open("sentimentValue.json", 'w') as f:
        json.dump(develop, f, indent=4)


