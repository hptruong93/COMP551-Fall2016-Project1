import datetime
import numpy as np

"""
    FeatureExtractor
    Features are:
    1) Gender: 0 for female, 1 for male, 2 for unknown
    2) Average marathon run time for each year in seconds
    3) Average non marathon run time for each year in seconds
    4) Count of marathon run for each year
    5) Count of non marathon run for each year


    Output paired with these should be:
        If run in the next year (1 = yes, 0 = no)
"""
def extract_features(data, years):
    # assert len(years) == 3

    ids = [row.runner_id for row in data]
    genders = [row.get_gender() for row in data]

    avg = lambda x : reduce(lambda a, b : a + b, x) / len(x) if len(x) > 0 else datetime.timedelta(seconds = 0)
    flatten_dict = lambda dictionary : [dictionary[key] for key in years]

    run_time_marathon = [{year : avg([marathon.time for marathon in row.marathons if marathon.in_year(year) and marathon.is_marathon()]).total_seconds() \
                        for year in years} \
                        for row in data]
    run_time_marathon = map(flatten_dict, run_time_marathon)

    run_time_non_marathon = [{year : avg([marathon.time for marathon in row.marathons if marathon.in_year(year) and not marathon.is_marathon()]).total_seconds() \
                        for year in years} \
                        for row in data]
    run_time_non_marathon = map(flatten_dict, run_time_non_marathon)

    marathon_count = [{year : len([marathon for marathon in row.marathons if marathon.in_year(year) and marathon.is_marathon()]) for year in years}  for row in data]
    marathon_count = map(flatten_dict, marathon_count)

    non_marathon_count = [{year : len([marathon for marathon in row.marathons if marathon.in_year(year) and not marathon.is_marathon()]) for year in years}  for row in data]
    non_marathon_count = map(flatten_dict, non_marathon_count)

    # Now concat the columns into X matrix
    X = []

    for index in xrange(len(data)):
        current_row = []
        for the_list in [ids, genders, run_time_marathon, run_time_non_marathon, marathon_count, non_marathon_count]:
            current = the_list[index]
            if type(current) is list:
                for item in current:
                    current_row.append(item)
            else:
                current_row.append(current)

        X.append(current_row)

    return np.array(X)