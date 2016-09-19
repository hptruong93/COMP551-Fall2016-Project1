
from LibraryLogisticRegression import LibraryLogisticRegression

if __name__ == "__main__":
	model = LibraryLogisticRegression() # Change this line to change model

	model.load_data()
	model.normalize()
	model.train()
	result = model.predict()

