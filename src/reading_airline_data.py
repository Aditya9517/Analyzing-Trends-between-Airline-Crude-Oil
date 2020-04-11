import pandas as pd
from src.retrieve_statistics import retrieve_stats
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches


def read_airline_data(airlines="../Data/airlines_IATA.csv"):
    """

    :param airlines:
    :return:
    """
    # Airlines
    # Next Phase is to determine the type of airlines operating in the United States

    airline_data = pd.read_csv(airlines)
    return airline_data


def airline_statistical_info(airline_data_frame):
    """

    :param airline_data_frame:
    :return:
    """
    # retrieve airline delays
    group = airline_data_frame['DEP_DELAY']
    statistics = group.groupby(airline_data_frame['OP_CARRIER'])
    statistics = statistics.apply(retrieve_stats).unstack()
    statistics = statistics.sort_values('Total Flights')
    return statistics


def visualize_airline_statistics(df, airline_data, airline_statistics):
    airline_companies = airline_data.set_index('IATA_CODE')['AIRLINE'].to_dict()

    font = {'family': 'normal', 'weight': 'bold', 'size': 15}

    df2 = df.loc[:, ['OP_CARRIER', 'DEP_DELAY']]
    df2['OP_CARRIER'] = df2['OP_CARRIER'].replace(airline_companies)

    colors = ['firebrick', 'gold', 'lightcoral', 'aquamarine', 'c', 'yellowgreen', 'grey',
              'seagreen', 'tomato', 'violet', 'wheat', 'chartreuse', 'lightskyblue', 'royalblue']
    ax3 = sns.stripplot(y="OP_CARRIER", x="DEP_DELAY", size=4, palette=colors, data=df2, linewidth=0.5, jitter=True)
    plt.setp(ax3.get_xticklabels(), fontsize=14)
    plt.setp(ax3.get_yticklabels(), fontsize=14)
    ax3.set_xticklabels(['{:2.0f}h{:2.0f}m'.format(*[int(y) for y in divmod(x, 60)]) for x in ax3.get_xticks()])
    plt.xlabel('Arrival Delay', fontsize=15, color='black')
    plt.ylabel('Airline', fontsize=15, color='black')
    ax3.yaxis.label.set_visible(False)
    plt.setp(ax3.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig('../Results/AirlineDelays.png', bbox_inches='tight')
    plt.close()








