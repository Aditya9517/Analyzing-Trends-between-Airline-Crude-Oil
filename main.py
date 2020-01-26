from argparse import ArgumentParser
from src.oil_prediction import date_conversion
import pandas as pd


def main():
    flag = 0
    parser = ArgumentParser()

    # source of crude oil data: Thomson Reuters
    parser.add_argument(
        "crudeOilFile",
        action="store",
        help="Description of historical oil prices per barrel")

    args = parser.parse_args()

    with open(args.crudeOilFile, 'r') as file:
        while flag < 4:
            next(file)
            flag += 1
        data = pd.read_csv(file, sep=',')

    date_conversion(data)



if __name__ == '__main__':
    main()
