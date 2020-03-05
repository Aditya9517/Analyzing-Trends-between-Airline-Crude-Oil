def retrieve_stats(data):
    return {'Total Flights': data.count(),
            'Maximum Departure Delay': data.max(),
            'Average Departure Delay': data.mean(),
            }
