

from abc import ABCMeta, abstractmethod

class AbstractClassifier(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_data():
        """
            Load raw data from appropriate csv file and store loaded data in internal state.
        """
        pass

    @abstractmethod
    def normalize():
        """
            Normalize (preprocess) the loaded data. This also splits the data into training set, evaluation set and test set.
        """
        pass

    @abstractmethod
    def train():
        """
            Train the internal model using the appropriate method.
            E.g. logistic regression using gradient descent or linear regression using closed form solution.
        """
        pass

    @abstractmethod
    def predict_single(runner_id):
        """
            Predict result for a single user.
            Input: runner_id (int) id of the runner
            Output: determined by the type of model (e.g. linear regression returns float, logistic regression returns boolean)
        """
        pass

    @abstractmethod
    def predict():
        """
            Perform prediction on all runners.
            Output: determined by the type of model.
        """
        pass

    @abstractmethod
    def evaluate():
        """
            Evaluate the trained model.
            Output: tuple containing two values: training error and test error (on test set)
        """
        pass