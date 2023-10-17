import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import pickle

def save_model():
    # Load dataset
    data = pd.read_excel("engine/data/thalassemia_3v_raw.xlsx")
    # Split dataset into features and target variable
    x = data.drop("DNA", axis=1)
    y = data["DNA"]
    # Split dataset into training and testing set
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=4
    )
    # Initialize Naive Bayes classifier
    model = GaussianNB()
    # Train the classifier
    model.fit(x_train, y_train)
    filename = "engine/model/nb_model.mod"
    pickle.dump(model, open(filename, "wb"))
    print("Model saved successfully")


def evaluate_model():
    # Load dataset
    data = pd.read_excel("engine/data/thalassemia_3v_raw.xlsx")
    # Split dataset into features and target variable
    x = data.drop("DNA", axis=1)
    y = data["DNA"]
    # Split dataset into training and testing set
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=4
    )
    # Initialize Naive Bayes classifier
    model = GaussianNB()
    # Train the classifier
    model.fit(x_train, y_train)
    # Memprediksi kelas data testing
    y_pred = model.predict(x_test)
    # Menghitung akurasi model
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(cm)
    print('accuracy', accuracy)
    print('precision', precision)
    print('recall', recall)
    print("Number of training data:", len(x_train))
    print("Number of testing data:", len(x_test))
    
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}



def check_probability(val):
    model = pickle.load(open("engine/model/nb_model.mod", "rb"))
    # Predict on the test set
    numpyArray = np.array([val])

    x_test = pd.DataFrame(data=numpyArray, columns=["HB", "MCV", "MCH"])
    y_pred = model.predict(x_test)
    
    probability = model.predict_proba(x_test)
    if y_pred[0] == 0:
        prob = (probability[0][0]) * 100
        return {"prediction": 0, "probability": prob}
    else:
        prob = (probability[0][1]) * 100
        return {"prediction": 1, "probability": prob}
