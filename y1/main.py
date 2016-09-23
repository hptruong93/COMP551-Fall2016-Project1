
from LibraryLogisticRegression import LibraryLogisticRegression
from ManualLogisticRegression import ManualLogisticRegression
import KFolder

k_fold = 50
OUTPUT_FILE = 'Y1.csv'

if __name__ == "__main__":
    model = LibraryLogisticRegression() # Change this line to change model
    # model = ManualLogisticRegression()

    data, X, y = model.load_data()
    X, y = model.normalize(X, y)

    folder = KFolder.KFolder(k_fold, X, y)

    train_errors = []
    test_errors = []

    for i in xrange(k_fold):
        X_train, y_train, X_test, y_test = folder.next()

        model.train(X_train, y_train)

        train_error = model.evaluate(X_train, y_train)
        test_error = model.evaluate(X_test, y_test)

        train_errors.append(train_error)
        test_errors.append(test_error)

    model.train(X, y)
    result = model.predict(data)

    avg = lambda x : sum(x) / float(len(x))
    print "Train/test errors: {0}, {1}".format(avg(train_errors), avg(test_errors))

    with open(OUTPUT_FILE, 'w') as f:
      for line in result:
          f.write(str(line))
          f.write('\n')