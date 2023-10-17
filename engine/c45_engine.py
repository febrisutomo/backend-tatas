import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import pickle
from utils import normalize_rule

def savemodel():
    # Load dataset
    data = pd.read_excel('engine/data/data.xls')
    # Split dataset into features and target variable
    X = data.drop('DNA', axis=1)
    y = data['DNA']
    # Fit decision tree classifier using C4.5 algorithm
    model = DecisionTreeClassifier(criterion='entropy')
   # Train the classifier
    model.fit(X, y)
    filename = 'engine/model/c45model.mod'
    pickle.dump(model, open(filename, 'wb'))


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

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    print('Hasil Confusion Matrix Model C4.5:')
    print("True Negative:", tn)
    print("False Positive:", fp)
    print("False Negative:", fn)
    print("True Positive:", tp)
    print('Nilai Accuracy', accuracy)
    print('Nilai Precision', precision)
    print('Nilai Recall', recall)


def cekkemungkinan(val, nama_model):
    model = pickle.load(open("engine/model/{}".format(nama_model), "rb"))
    # Predict on the test set
    norm = normalize_rule.normalisasi(val)
    numpyArray = np.array([norm])
    X3 = pd.DataFrame(data=numpyArray, columns=["HB", "MCV", "MCH"])
    y2 = [1]
    y_pred = model.predict(X3)
    probabilitas = model.predict_proba(X3)
    hasil = ""
    if y_pred[0] == 0:
        prob = (probabilitas[0][0]) * 100
        return {"prediksi": 0, "probabilitas": prob}
    else:
        prob = (probabilitas[0][1]) * 100
        return {"prediksi": 1, "probabilitas": prob}

def create_model(data_periksa, nama_model):
    data_baru = pd.DataFrame.from_records(data_periksa, exclude=[
                                          'id', 'user_id', 'date', 'prediction', 'probability', 'verified'])
    # normalisasi HB
    norm1 = data_baru['hb'] < 12
    norm2 = data_baru['hb'] >= 12
    data_baru.loc[norm1, 'hb'] = 1
    data_baru.loc[norm2, 'hb'] = 0
    
    # normalisasi MCV
    norm3 = data_baru['mcv'] < 80
    norm4 = data_baru['mcv'] >= 80
    data_baru.loc[norm3, 'mcv'] = 1
    data_baru.loc[norm4, 'mcv'] = 0

    # normalisasi MCH
    norm5 = data_baru['mch'] < 27
    norm6 = data_baru['mch'] >= 27
    data_baru.loc[norm5, 'mch'] = 1
    data_baru.loc[norm6, 'mch'] = 0

    data_baru.rename(columns= {'hb':'HB', 'mcv':'MCV', 'mch':'MCH', 'dna':'DNA'}, inplace=True)

    data_excel = pd.read_excel('engine/data/data.xls')
    data = pd.concat([data_excel, data_baru])
    X = data.drop('DNA', axis=1)
    y = data['DNA']
    # Fit decision tree classifier using C4.5 algorithm
    model = DecisionTreeClassifier(criterion='entropy')
    # Train the classifier
    model.fit(X, y)
    filename = 'engine/model/{}'.format(nama_model)
    pickle.dump(model, open(filename, 'wb'))