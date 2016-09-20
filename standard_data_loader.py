
import csv
import datetime

import numpy as np

to_date = lambda string : datetime.datetime.strptime(string, '%Y-%m-%d')

def to_time_delta(string):
    """
        Convert a marathon duration to time delta object.
        Input: duration in form "hh:mm:ss", or "-1"
        Output: according time delta object, or 0 if "-1" is input
    """
    split = [int(x) for x in string.split(':')]
    if len(split) != 3:
        split = [0,0,0]
    return datetime.timedelta(hours = split[0], minutes = split[1], seconds = split[2])

FIRST_COLUMN = 'PARTICIPANT ID'
COLUMNS = ['EVENT DATE', 'EVENT NAME', 'EVENT TYPE', 'TIME', 'CATEGORY']

FILE_NAME = 'Project1_data.csv'

class Marathon(object):
    """Represent a marathon run"""
    def __init__(self):
        super(Marathon, self).__init__()
        self.date = None
        self.name = None
        self.event_type = None
        self.time = None
        self.category = None

    def is_marathon(self):
        return self.event_type.lower() == "Marathon"

    def in_year(self, year):
        return self.date.year == year

class Runner(object):
    """Represent a marathon Runner"""
    def __init__(self):
        super(Runner, self).__init__()
        self.runner_id = None
        self.marathons = None

    def get_gender(self):
        male_set = ['M' for marathon in self.marathons if marathon.category.startswith('M')]
        female_set = ['F' for marathon in self.marathons if marathon.category.startswith('F')]
        unknown_set = ['U' for marathon in self.marathons if not marathon.category.startswith('M') and not marathon.category.startswith('F')]

        sets = [male_set, female_set, unknown_set]

        output = sets[np.argmax(map(len, sets))][0]
        return 0 if output == 'F' else 1 if output == 'M' else 2


def _row_process(row):
    """
        Read a row and load the runner id as well as the marathon he has run.
        Output: runner id as int and the list of marathons.
    """
    count = 0
    marathons = []

    while count < len(row):
        # Skip first column
        if count == 0:
            count += 1
            continue

        new_run = Marathon()
        new_run.date = to_date(row[count])
        new_run.name = row[count + 1]
        new_run.event_type = row[count + 2]
        new_run.time = to_time_delta(row[count + 3])
        new_run.category = row[count + 4]

        marathons.append(new_run)
        count += len(COLUMNS)

    output = Runner()
    output.runner_id = int(row[0])
    output.marathons = marathons
    return output


def load_data(file_name = FILE_NAME):
    count = 0
    with open(file_name, 'r') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0) # rewind

        reader = csv.reader(csvfile, delimiter = ',')
        if has_header:
            next(reader)

        data = [_row_process(row) for row in reader]
        return data

if __name__ == "__main__":
    load_data()
