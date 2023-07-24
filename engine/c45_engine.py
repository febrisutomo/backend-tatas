import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pickle


def savemodel():
    # Load dataset
    data = pd.read_excel("engine/data/data.xls")
    # Split dataset into features and target variable
    X = data.drop("DNA", axis=1)
    y = data["DNA"]
    # Fit decision tree classifier using C4.5 algorithm
    model = DecisionTreeClassifier(criterion="entropy")
    # Train the classifier
    model.fit(X, y)
    filename = "engine/model/c45_model.mod"
    pickle.dump(model, open(filename, "wb"))


def testtrain():
    # Load dataset
    data = pd.read_excel("engine/data/data.xls")
    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop("DNA", axis=1), data["DNA"], test_size=0.3, random_state=42
    )
    # Fit decision tree classifier using C4.5 algorithm
    clf = DecisionTreeClassifier(criterion="entropy")
    # Train the model
    clf.fit(X_train, y_train)
    # Make predictions on testing set
    y_pred = clf.predict(X_test)
    # Calculate accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    print('c45')
    print('accuracy', accuracy)
    print('precision', precision)
    print('recall', recall)


def cekkemungkinan(val):
    model = pickle.load(open("engine/model/c45_model.mod", "rb"))
    # Predict on the test set
    numpyArray = np.array([val])
    X3 = pd.DataFrame(data=numpyArray, columns=["HB", "MCV", "MCH"])
    y2 = [1]
    y_pred = model.predict(X3)
    probabilitas = model.predict_proba(X3)
    hasil = ""
    if y_pred[0] == 0:
        prob = (probabilitas[0][0]) * 100
        return {"prediksi": "Negatif", "probabilitas": prob}
    else:
        prob = (probabilitas[0][1]) * 100
        return {"prediksi": "Positif", "probabilitas": prob}
