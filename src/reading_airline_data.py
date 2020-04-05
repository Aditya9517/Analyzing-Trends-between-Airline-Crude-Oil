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
    abbr_companies = airline_data.set_index('IATA_CODE')['AIRLINE'].to_dict()

    font = {'family': 'normal', 'weight': 'bold', 'size': 15}

    df2 = df.loc[:, ['OP_CARRIER', 'DEP_DELAY']]
    df2['OP_CARRIER'] = df2['OP_CARRIER'].replace(abbr_companies)

    colors = ['royalblue', 'grey', 'wheat', 'c', 'firebrick', 'seagreen', 'lightskyblue',
              'lightcoral', 'yellowgreen', 'gold', 'tomato', 'violet', 'aquamarine', 'chartreuse']

    # fig = plt.figure(1, figsize=(16, 15))
    # gs = GridSpec(2, 2)
    # ax1 = fig.add_subplot(gs[0, 0])
    # ax2 = fig.add_subplot(gs[0, 1])
    # ax3 = fig.add_subplot(gs[1, :])
    #
    labels = [s for s in airline_statistics.index]
    #
    # sizes = airline_statistics['Total Flights'].values
    #
    # explode = [0.3 if sizes[i] < 20000 else 0.0 for i in range(len(abbr_companies))]
    #
    # patches, texts, autotexts = ax1.pie(sizes, explode=explode,
    #                                     labels=labels, colors=colors, autopct='%1.0f%%',
    #                                     shadow=False, startangle=0)
    # for i in range(len(abbr_companies)):
    #     texts[i].set_fontsize(14)
    # ax1.axis('equal')
    # ax1.set_title('% of flights per company', bbox={'facecolor': 'midnightblue', 'pad': 5},
    #               color='w', fontsize=18)

    # comp_handler = []
    # for i in range(len(abbr_companies)):
    #     comp_handler.append(mpatches.Patch(color=colors[i], label=airline_statistics.index[i] + ': ' +
    #                                                               abbr_companies[airline_statistics.index[i]]))
    # ax1.legend(handles=comp_handler, bbox_to_anchor=(0.2, 0.9),
    #            fontsize=13, bbox_transform=plt.gcf().transFigure)

    # sizes = airline_statistics['Average Departure Delay'].values
    # sizes = [max(s, 0) for s in sizes]
    # explode = [0.0 if sizes[i] < 20000 else 0.01 for i in range(len(abbr_companies))]
    # patches, texts, autotexts = ax2.pie(sizes, explode=explode, labels=labels, colors=colors, shadow=False, startangle=0,
    #                                     autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100))
    # for i in range(len(abbr_companies)):
    #     texts[i].set_fontsize(14)
    # ax2.axis('equal')
    # ax2.set_title('Mean delay at origin', bbox={'facecolor': 'midnightblue', 'pad': 5}, color='w', fontsize=18)
    colors = ['firebrick', 'gold', 'lightcoral', 'aquamarine', 'c', 'yellowgreen', 'grey',
              'seagreen', 'tomato', 'violet', 'wheat', 'chartreuse', 'lightskyblue', 'royalblue']
    ax3 = sns.stripplot(y="OP_CARRIER", x="DEP_DELAY", size=4, palette=colors, data=df2, linewidth=0.5, jitter=True)
    plt.setp(ax3.get_xticklabels(), fontsize=14)
    plt.setp(ax3.get_yticklabels(), fontsize=14)
    ax3.set_xticklabels(['{:2.0f}h{:2.0f}m'.format(*[int(y) for y in divmod(x, 60)]) for x in ax3.get_xticks()])
    plt.xlabel('Departure delay', fontsize=15, color='black')
    ax3.yaxis.label.set_visible(False)
    plt.setp(ax3.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig('../Results/AirlineDelays.png', bbox_inches='tight')
    plt.close()
