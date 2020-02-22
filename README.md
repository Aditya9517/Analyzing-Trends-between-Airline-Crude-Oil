# Analyzing-Trends-between-Airline-Crude-Oil

### Background
The airline industry is very competitive and has a very small profit margin. Within the past year, nearly twenty-four 
airlines all over the world have gone out of business. While prices fluctuate drastically over a short period, some of 
the key factors that influence costs are stock markets and crude oil prices. In addition, airlines may need to 
compensate passengers for flight delays, cancellations or overbooking and this may impact ticket prices. The objective 
of this capstone project is to utilize existing knowledge and gain a wider perspective on how variation in crude oil 
prices affect airlines using Machine Learning and Natural Language Processing.

### Prerequisites

Data for this project is stored as a csv in [Data](https://github.com/Aditya9517/Analyzing-Trends-between-Airline-Crude-Oil/tree/master/Data)

Required libraries are defined in [requirements.txt](https://github.com/Aditya9517/Analyzing-Trends-between-Airline-Crude-Oil/blob/master/requirements.txt)

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

