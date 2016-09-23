import numpy as np
from sklearn.cross_validation import train_test_split

class KFolder(object):
	"""
		Implementation of K Fold data provider. Split data into k roughly equal parts.
		At each fold the folder provides k - 1 parts for training and 1 part for validation.
	"""
	def __init__(self, k, X, y):
		super(KFolder, self).__init__()
		self.k = k
		self.Xs = []
		self.ys = []

		portion_size = len(y) / float(k)

		for i in xrange(self.k - 1):
			test_percentage = portion_size / len(y)
			X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_percentage, random_state = 69) # This random split implementation is trivial.

			X = X_train
			y = y_train

			self.Xs.append(X_test)
			self.ys.append(y_test)

		self.Xs.append(X)
		self.ys.append(y)

		self.index = -1

	def next(self):
		"""
			Get the next fold used for training and cross validation.
			Output: the next fold of X train, y train, X validation, y validation
		"""
		self.index += 1
		return np.vstack([x for i, x in enumerate(self.Xs) if i != self.index]), np.array([item for i, y in enumerate(self.ys) if i != self.index for item in y]),\
				self.Xs[self.index], self.ys[self.index]