# Import library pandas untuk manipulasi data
import pandas as pd
# Import library numpy untuk operasi numerik
import numpy as np
# Import class GaussianNB dari library sklearn untuk Naive Bayes
from sklearn.naive_bayes import GaussianNB
# Import fungsi train_test_split dari library sklearn untuk membagi dataset
from sklearn.model_selection import train_test_split
# Import beberapa metrik evaluasi dari sklearn
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
# Import library pickle untuk menyimpan dan membaca model
import pickle

# Fungsi untuk menyimpan model yang sudah dilatih
def save_model():
    # Memuat dataset
    data = pd.read_excel("engine/data/thalassemia_3v_raw.xlsx")
    # Memisahkan dataset menjadi fitur-fitur dan variabel target
    x = data.drop("DNA", axis=1)
    y = data["DNA"]
    # Memisahkan dataset menjadi data latih dan data uji
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=42
    )
    # Inisialisasi klasifikasi Naive Bayes
    model = GaussianNB()
    # Melatih klasifikasi
    model.fit(x_train, y_train)
    # Nama file untuk menyimpan model
    filename = "engine/model/nb_model.mod"
    # Menyimpan model dalam file menggunakan pickle
    pickle.dump(model, open(filename, "wb"))

# Fungsi untuk mengevaluasi kinerja model yang sudah dilatih
def evaluate_model():
    # Memuat dataset
    data = pd.read_excel("engine/data/thalassemia_3v_raw.xlsx")
    # Memisahkan dataset menjadi fitur-fitur dan variabel target
    x = data.drop("DNA", axis=1)
    y = data["DNA"]
    # Memisahkan dataset menjadi data latih dan data uji
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=42
    )
    # Inisialisasi klasifikasi Naive Bayes
    model = GaussianNB()
    # Melatih klasifikasi
    model.fit(x_train, y_train)
    # Memprediksi kelas data uji
    y_pred = model.predict(x_test)
    # Menghitung metrik kinerja model
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("Confusion Matrix:")
    print(cm)
    print('Akurasi:', accuracy)
    print('Presisi:', precision)
    print('Recall:', recall)
    
    return {"Akurasi": accuracy, "Presisi": precision, "Recall": recall, "F1": f1}

# Fungsi untuk memeriksa probabilitas prediksi
def check_probability(val):
    # Memuat model yang sudah disimpan sebelumnya
    model = pickle.load(open("engine/model/nb_model.mod", "rb"))
    # Mengubah data input menjadi array NumPy
    numpyArray = np.array([val])
    # Mengubah array menjadi DataFrame dengan kolom yang sesuai
    x_test = pd.DataFrame(data=numpyArray, columns=["HB", "MCV", "MCH"])
    # Memprediksi kelas data uji
    y_pred = model.predict(x_test)
    # Menghitung probabilitas prediksi
    probability = model.predict_proba(x_test)
    if y_pred[0] == 0:
        prob = (probability[0][0]) * 100  # Menghitung probabilitas kelas 0
        return {"prediksi": 0, "probabilitas": prob}
    else:
        prob = (probability[0][1]) * 100  # Menghitung probabilitas kelas 1
        return {"prediksi": 1, "probabilitas": prob}
