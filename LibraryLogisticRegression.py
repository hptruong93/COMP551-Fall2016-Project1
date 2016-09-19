
import numpy as np
import AbstractClassifier

class LibraryLogisticRegression(AbstractClassifier.AbstractClassifier):
    """Logistic regression using scikit-learn"""
    def __init__(self):
        super(LibraryLogisticRegression, self).__init__()

    def load_data():
        """
            Load raw data from appropriate csv file and store loaded data in internal state.
        """
        pass

    def normalize():
        """
            Normalize (preprocess) the loaded data.
        """
        pass

    def train():
        """
            Train the internal model using the appropriate method.
            E.g. logistic regression using gradient descent or linear regression using closed form solution.
        """
        pass

    def predict_single(runner_id):
        """
            Predict result for a single user.
            Input: runner_id (int) id of the runner
            Output: determined by the type of model (e.g. linear regression returns float, logistic regression returns boolean)
        """
        pass

    def predict():
        """
            Perform prediction on all runners.
            Output: determined by the type of model.
        """
        pass