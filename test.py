from bs4 import BeautifulSoup
import requests
from newspaper import Article


if __name__ == '__main__':
    input_file = {}
    URL = "https://oilprice.com/Latest-Energy-News/World-News/"
    req = requests.get(URL)
    soup = BeautifulSoup(req.content, 'html.parser')

    count = 0

    last_page = soup.find(class_="num_pages").text[1:]

    for i in range(int(last_page)):
        count += 1
        url = URL + "Page-" + str(count) + ".html"
        print(url)
        soup1 = BeautifulSoup(requests.get(url).content, features="lxml")
        main_div = soup1.select_one("div.tableGrid__column.tableGrid__column--articleContent.category")
        divs = main_div.select('div.categoryArticle__content')
        links = [(d.select_one("p.categoryArticle__meta").text.split("|")[0].strip(), d.a["href"]) for d in divs]


