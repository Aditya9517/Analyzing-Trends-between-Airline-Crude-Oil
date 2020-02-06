from argparse import ArgumentParser
from src.oil_prediction import read_data
from src.sentiment_analysis_news_articles import news_article_sentiment
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

    # read_data(args.crudeOilFile)
    news_article_sentiment(args.crudeOilNews)


if __name__ == '__main__':
    main()
