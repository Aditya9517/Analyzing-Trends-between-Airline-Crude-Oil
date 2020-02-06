from bs4 import BeautifulSoup
import requests
import json
from newspaper import Article
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_web_page_link(url="https://oilprice.com/Latest-Energy-News/World-News/"):
    links = []
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # to find the last page of the website dynamically
    last_page = soup.find(class_="num_pages").text[1:]

    # To simplify the process, based on earlier analysis a spike was observed during between 2008-2012
    # web scraping is performed to retrieve news articles during that time

    for i in range(565, 932):
        url = url + "Page-" + str(i) + ".html"
        soup = BeautifulSoup(requests.get(url).content, features="lxml")
        main_div = soup.select_one("div.tableGrid__column.tableGrid__column--articleContent.category")
        divs = main_div.select('div.categoryArticle__content')
        links += [(d.select_one("p.categoryArticle__meta").text.split("|")[0].strip(), d.a["href"]) for d in divs]
        url = "https://oilprice.com/Latest-Energy-News/World-News/"
    return links


def scrape_news_articles(web_page_links):
    news_articles = {}
    for i in range(len(web_page_links)):
        article = Article(web_page_links[i][1])
        date = web_page_links[i][0]
        date = date.replace("at", "")
        date = date.replace(",", "")
        datetime_object = datetime.strptime(date, '%b %d %Y %H:%M')
        article.download()
        article.parse()
        news_articles[str(datetime_object)] = article.text

    with open('ScrapedNewsArticles/oil_news.json', 'w') as news:
        json.dump(news_articles, news, indent=4)


if __name__ == '__main__':
    scrape_news_articles(get_web_page_link())
    # print(get_web_page_link())

