
import random
import datetime
import time
import math
import sys

import numpy as np
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split

import feature_extractor
import LibraryLogisticRegression


def write_stdout(x):
    sys.stdout.write(x)
    sys.stdout.flush()

sigmoid = lambda x : 1.0 / (1.0 + np.exp(-x))

class _InnerModel(object):
    """
        Implementation of Logistic regression.
    """

    THRESHOLD = 0.5
    DEFAULT_STEP = 0.01
    REDUCTION_FACTOR = 0.75
    COST_THRESHOLD = 0.000001

    def __init__(self):
        super(_InnerModel, self).__init__()
        self.m = 0 # Number of features
        self.n = 0 # Number of samples
        self.coeficients = None # This is m x 1 matrix where m is the number of features

    def _generate_alpha(self):
        return self.step

    def _cost(self, X, y):
        """
            Calculate the cost function using the current coeficients.
            Input: X matrix with m columns, y array with n samples
            Output: logistic regression cost function
        """
        h = sigmoid(X.dot(self.coeficients))
        cost1 = y * np.log(h)
        cost2 = (1 - y) * np.log(1 - h)
        return np.mean(-cost1 -cost2)

    def fit(self, X, y):
        """
            Perform gradient descent to optimize for appropriate weights of the model. Automatically determine m and n from matrix X
            Learning rate starts at a default value, and is halved every time the cost function increases.

            Input: Column normalized X matrix of n rows and m columns, y array with n rows
            Output: None
        """
        self.step = _InnerModel.DEFAULT_STEP
        self.m = X.shape[1] + 1 # Add 1 to take into account of constant intercept
        self.n = X.shape[0]

        print "m is {0} and n is {1}".format(self.m, self.n)

        X = np.insert(X, 0, 1, axis = 1) # Add columns of 1s in the front
        y = np.array([[val] for val in y])

        # Initiate weight randomly
        self.coeficients = np.array([[random.random()] for _ in xrange(0, self.m)])

        old_cost = None
        i = 0
        while True:
            write_stdout("\rIteration {0}... ".format(i))
            i += 1

            start = time.time()

            ##############################################################################################################################################
            ################################################### The actual computation section ###########################################################
            ##############################################################################################################################################
            delta = X.T.dot(y - sigmoid(X.dot(self.coeficients)))
            self.coeficients = self.coeficients + self._generate_alpha() * delta

            norm = np.linalg.norm(delta)
            new_cost = self._cost(X, y)
            ##############################################################################################################################################

            write_stdout("Cost is %s and norm of delta is %s. " % (str(new_cost), str(norm)))
            write_stdout("Took {0}s".format(time.time() - start))

            if old_cost is not None and abs(new_cost - old_cost) < _InnerModel.COST_THRESHOLD:
                break
            elif new_cost > old_cost:
                self.step = self.step * _InnerModel.REDUCTION_FACTOR

            old_cost = new_cost

        print ""

    def predict(self, data):
        """
            Perform prediction using the current coefficients.
            Input: data matrix with m columns for m features.
            Output: array of predictions for each input row.
        """
        data = np.insert(data, 0, 1, axis = 1) # Add columns of 1s in the front
        probabilities = sigmoid(np.dot(data, self.coeficients))
        return [1 if p >= _InnerModel.THRESHOLD else 0 for p in probabilities]

    def score(self, data, result):
        """
            Perform scoring (evaluation) using the current coefficients.
            Input: data matrix with m columns, true result as an array having the result for each data row.
            Output: the accuracy of the model, between 0 and 1.
        """
        predicted = self.predict(data)
        correct_count = len([x for index, x in enumerate(predicted) if x == result[index]])

        return float(correct_count) / len(result)


class ManualLogisticRegression(LibraryLogisticRegression.LibraryLogisticRegression):
    """Logistic regression using scikit-learn"""
    def __init__(self):
        super(ManualLogisticRegression, self).__init__()
        self.data = None

    def normalize(self, X, y):
        X = preprocessing.normalize(X, axis = 0) # Normalize the features to have 0 mean and unit variance
        return X, y

    def train(self, X, y):
        self.model = _InnerModel()

        start = time.time()
        self.model.fit(X, y)
        print "Training took {0}s".format(time.time() - start)

    def predict(self, data):
        X_predict = feature_extractor.extract_features(data, LibraryLogisticRegression._PREDICTING_YEARS)
        X_predict = preprocessing.normalize(X_predict, axis = 0) # Normalize the features to have 0 mean and unit variance
        return self.model.predict(X_predict)