
import datetime

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

import AbstractClassifier
import standard_data_loader

"""
    Features are:
        1) Gender: 0 for female, 1 for male, 2 for unknown
        2) Average marathon run time 2012, 2013, 2014, 2015 in seconds
        3) Average non marathon run time 2012, 2013, 2014, 2015 in seconds
        4) Count of marathon run in 2012, 2013, 2014, 2015
        5) Count of non marathon run in 2012, 2013, 2014, 2015


    Output is:
        If run in 2015 (1 = yes, 0 = no)
"""

_YEARS = [year for year in xrange(2012, 2016)]

class LibraryLogisticRegression(AbstractClassifier.AbstractClassifier):
    """Logistic regression using scikit-learn"""
    def __init__(self):
        super(LibraryLogisticRegression, self).__init__()
        self.data = None

    def load_data(self):
        """
            Load raw data from appropriate csv file and store loaded data in internal state.
        """
        self.data = standard_data_loader.load_data()

        ##################################################################################################################################################################
        ######################################################## Now transform the data into the features ################################################################
        ##################################################################################################################################################################
        ids = [row.runner_id for row in self.data]
        genders = [row.get_gender() for row in self.data]

        avg = lambda x : reduce(lambda a, b : a + b, x) / len(x) if len(x) > 0 else datetime.timedelta(seconds = 0)
        flatten_dict = lambda dictionary : [dictionary[key] for key in xrange(2012, 2016)]

        run_time_marathon = [{year : avg([marathon.time for marathon in row.marathons if marathon.in_year(year) and marathon.is_marathon()]).total_seconds() \
                            for year in xrange(2012, 2016)} \
                            for row in self.data]
        run_time_marathon = map(flatten_dict, run_time_marathon)

        run_time_non_marathon = [{year : avg([marathon.time for marathon in row.marathons if marathon.in_year(year) and not marathon.is_marathon()]).total_seconds() \
                            for year in xrange(2012, 2016)} \
                            for row in self.data]
        run_time_non_marathon = map(flatten_dict, run_time_non_marathon)

        marathon_count = [{year : len([marathon for marathon in row.marathons if marathon.in_year(year) and marathon.is_marathon()]) for year in xrange(2012, 2016)}  for row in self.data]
        marathon_count = map(flatten_dict, marathon_count)

        non_marathon_count = [{year : len([marathon for marathon in row.marathons if marathon.in_year(year) and not marathon.is_marathon()]) for year in xrange(2012, 2016)}  for row in self.data]
        non_marathon_count = map(flatten_dict, non_marathon_count)
        ##################################################################################################################################################################
        ##################################################################################################################################################################

        # Calculate output
        whether_run_2015 = [1 if sum(1 for marathon in row.marathons if marathon.in_year(2015)) > 0 else 0 for row in self.data]

        # Now concat the columns into X matrix
        self.X = []

        for index in xrange(len(self.data)):
            current_row = []
            for the_list in [ids, genders, run_time_marathon, run_time_non_marathon, marathon_count, non_marathon_count]:
                current = the_list[index]
                if type(current) is list:
                    for item in current:
                        current_row.append(item)
                else:
                    current_row.append(current)

            self.X.append(current_row)

        self.y = whether_run_2015

        assert len(self.X) == len(self.y)

    def normalize(self):
        """
            Normalize (preprocess) the loaded data. This also splits the data into training set, evaluation set and test set.
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size = 0.2, random_state = 69)
        self.X = None
        self.y = None

    def train(self):
        """
            Train the internal model using the appropriate method.
            E.g. logistic regression using gradient descent or linear regression using closed form solution.
        """
        self.model = LogisticRegression()
        self.model.fit(self.X_train, self.y_train)

    def predict_single(self, runner_id):
        """
            Predict result for a single user.
            Input: runner_id (int) id of the runner
            Output: determined by the type of model (e.g. linear regression returns float, logistic regression returns boolean)
        """
        pass

    def predict(self):
        """
            Perform prediction on all runners.
            Output: determined by the type of model.
        """
        pass

    def evaluate(self):
        """
            Evaluate the trained model.
            Output: tuple containing two values: training error and test error (on test set)
        """
        train_error = 1 - self.model.score(self.X_train, self.y_train)
        test_error = 1 - self.model.score(self.X_test, self.y_test)

        return train_error, test_error