from argparse import ArgumentParser
from src.oil_price_trend import read_data
from src.sentiment_analysis_news_articles import news_article_sentiment
from src.analyze_flight_data_2016 import read_combined_data
import warnings


def main():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    parser = ArgumentParser()
    # source of crude oil data: Thomson Reuters
    parser.add_argument(
        "crudeOilFile",
        action="store",
        help="Description of historical oil prices per barrel")

    # source of crude oil news: www.oilprice.com
    parser.add_argument(
        "crudeOilNews",
        action="store",
        help="Collection of news articles")

    args = parser.parse_args()

    data_oil = read_data(args.crudeOilFile)
    news_article_sentiment(data_oil, args.crudeOilNews)
    read_combined_data()


if __name__ == '__main__':
    main()
