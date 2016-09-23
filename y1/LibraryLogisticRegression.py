
import datetime

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split

import AbstractClassifier
import standard_data_loader
import feature_extractor

_TRAINING_YEARS = list(xrange(2012, 2015))
_PREDICTING_YEARS = list(xrange(2013, 2016))


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
        self.X = feature_extractor.extract_features(self.data, _TRAINING_YEARS)
        ##################################################################################################################################################################
        ##################################################################################################################################################################

        # Calculate output
        whether_run = [1 if sum(1 for marathon in row.marathons if marathon.in_year(2015)) > 0 else 0 for row in self.data]
        self.y = np.array(whether_run)

        assert len(self.X) == len(self.y)

    def normalize(self):
        """
            Normalize (preprocess) the loaded data. This also splits the data into training set, evaluation set and test set.
        """
        # No need to normalize. Library is good enough to handle this.
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

        print self.model.coef_
        print self.model.intercept_

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
        X_predict = feature_extractor.extract_features(self.data, _PREDICTING_YEARS)
        return self.model.predict(X_predict)

    def evaluate(self):
        """
            Evaluate the trained model.
            Output: tuple containing two values: training error and test error (on test set)
        """
        train_error = 1 - self.model.score(self.X_train, self.y_train)
        test_error = 1 - self.model.score(self.X_test, self.y_test)

        return train_error, test_error