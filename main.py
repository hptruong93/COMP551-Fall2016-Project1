
from LibraryLogisticRegression import LibraryLogisticRegression
from ManualLogisticRegression import ManualLogisticRegression

OUTPUT_FILE = 'Y1.csv'

if __name__ == "__main__":
	# model = LibraryLogisticRegression() # Change this line to change model
	model = ManualLogisticRegression()

	model.load_data()
	model.normalize()
	model.train()
	result = model.predict()

	errors = model.evaluate()
	print "Train, test errors are {0}".format(errors)

	with open(OUTPUT_FILE, 'w') as f:
		for line in result:
			f.write(str(line))
			f.write('\n')