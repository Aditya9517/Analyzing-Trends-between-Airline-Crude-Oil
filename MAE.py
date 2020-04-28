# Load the Pandas libraries with alias 'pd'
import pandas as pd

from sklearn.metrics import mean_absolute_error


if __name__ == '__main__':
    data = pd.read_csv(
        "/Users/adityakalyanjayanti/PycharmProjects/Analyzing-Trends-between-Airline-Crude-Oil/Data/2018.csv")

    result = mean_absolute_error(data['Original'], data['Predicted'])

    result1 = mean_absolute_error(data['Original'], data['DCOILWTICO'])


    print(result)
    print(result1)




