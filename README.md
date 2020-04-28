# Analyzing-Trends-between-Airline-Crude-Oil

### Background
The airline industry is very competitive and has a very small profit margin. Within the past year, nearly twenty-four 
airlines all over the world have gone out of business. While prices fluctuate drastically over a short period, some of 
the key factors that influence costs are stock markets and crude oil prices. In addition, airlines may need to 
compensate passengers for flight delays, cancellations or overbooking and this may impact ticket prices. The objective 
of this capstone project is to utilize existing knowledge and gain a wider perspective on how variation in crude oil 
prices affect airlines using Machine Learning and Natural Language Processing.

### Prerequisites

Data for this project is stored as a csv in [Data](https://drive.google.com/drive/folders/1mS6ugNkT0UXWv9HV6VZMFVCkSpdPNe8X?usp=sharing)

Required libraries are defined in [requirements.txt](https://github.com/Aditya9517/Analyzing-Trends-between-Airline-Crude-Oil/blob/master/requirements.txt)

Software to be installed:
* Anaconda Python 3.7
* Python3

Additionally, the following Python modules are required:
* numpy
* pandas
* matplotlib
* sklearn
* keras
* mpl_toolkits
* newspaper3k
* datetime
* BeautifulSoup
* json
* requests
* OrderedDict
* wordcloud
* statsmodels
* nltk.sentiment.vader
* wordcloud
* fbprophet
* seaborn


## Installing Dependencies
```
pip3 install -r requirements.txt
```

### Running the code

A web scraper is used to retrieve news articles from https://oilprice.com/, it is filtered to retrieve articles 
specifically relating to crude oil news. 

```
python3 scrape_oil_news.py
```

Collating on time flight performance data (2016)

```
python3 collate_flight_data.py
```

Main file executes oil_price_trend.py, oil_price_trend_specific.py, sentiment_analyis_news_articles, analyze_flight_data_2016,and 
reading_airline_data.py

```
python3 main.py
```



