
import datetime

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing

import AbstractClassifier
import standard_data_loader
import feature_extractor

_TRAINING_YEARS = list(xrange(2012, 2015))
_PREDICTING_YEARS = list(xrange(2013, 2016))


class LibraryLogisticRegression(AbstractClassifier.AbstractClassifier):
    """Logistic regression using scikit-learn"""
    def __init__(self):
        super(LibraryLogisticRegression, self).__init__()

    def load_data(self):
        data = standard_data_loader.load_data()

        ##################################################################################################################################################################
        ######################################################## Now transform the data into the features ################################################################
        ##################################################################################################################################################################
        X = feature_extractor.extract_features(data, _TRAINING_YEARS)
        ##################################################################################################################################################################
        ##################################################################################################################################################################

        # Calculate output
        whether_run = [1 if sum(1 for marathon in row.marathons if marathon.in_year(2015)) > 0 else 0 for row in data]
        y = np.array(whether_run)

        assert len(X) == len(y)

        return data, X, y

    def normalize(self, X, y):
        # No need to normalize. Library is good enough to handle this.
        return X, y

    def train(self, X_train, y_train):
        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)

    def predict_single(self, runner_id):
        pass

    def predict(self, data):
        X_predict = feature_extractor.extract_features(data, _PREDICTING_YEARS)
        return self.model.predict(X_predict)

    def evaluate(self, X, y):
        return 1 - self.model.score(X, y)
