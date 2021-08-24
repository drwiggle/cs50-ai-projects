import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

def main():
    if len(sys.argv) != 2:
        sys.exit("Correct usage: python myshopping.py data")

    # Load data from spreadsheet
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size = TEST_SIZE
    )

    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = model.evaluate(y_test, predictions)
    
if __name__ == "__main__":
    main()
