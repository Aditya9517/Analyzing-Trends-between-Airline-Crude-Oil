from argparse import ArgumentParser
from src.oil_prediction import read_data


def main():
    parser = ArgumentParser()
    # source of crude oil data: Thomson Reuters
    parser.add_argument(
        "crudeOilFile",
        action="store",
        help="Description of historical oil prices per barrel")
    args = parser.parse_args()
    read_data(args.crudeOilFile)


if __name__ == '__main__':
    main()
