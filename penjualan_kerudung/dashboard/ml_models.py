import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from .models import ProcessingDataLatih, ModelPerformance
import matplotlib.pyplot as plt
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import train_test_split

# Fungsi untuk melatih model


def train_model():
    # Ambil data dari database
    data = ProcessingDataLatih.objects.all().values(
        'brand', 'jenis', 'bahan', 'harga', 'terjual')
    df = pd.DataFrame(data)

    # Encode categorical variables
    df_encoded = pd.get_dummies(
        df[['brand', 'jenis', 'bahan', 'harga']])
    X = df_encoded
    y = df['terjual']

    # Bagi data menjadi training dan testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Latih decision tree
    clf = DecisionTreeClassifier(criterion='entropy')
    clf = clf.fit(X_train, y_train)

    # Prediksi data testing
    y_pred = clf.predict(X_test)

    # Hitung metrik evaluasi
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    # Hapus data performa lama
    ModelPerformance.objects.all().delete()

    # Simpan metrik ke database
    ModelPerformance.objects.create(
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=f1
    )

    # Cetak nilai metrik
    print("Akurasi:", accuracy)
    print("Presisi:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)

    return clf, X.columns


def predict_sales(model, feature_columns, input_data):
    df_input = pd.DataFrame([input_data])
    df_input_encoded = pd.get_dummies(df_input)
    df_input_encoded = df_input_encoded.reindex(
        columns=feature_columns, fill_value=0)
    prediction = model.predict(df_input_encoded)
    return prediction[0]

# Fungsi untuk visualisasi pohon keputusan


def plot_tree(model, feature_names, class_names):
    fig = plt.figure(figsize=(34, 17), dpi=300)
    _ = tree.plot_tree(model, feature_names=feature_names, class_names=class_names,
                       filled=True, rounded=True, fontsize=12)

    # Simpan gambar di folder static
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    plt.savefig(os.path.join(static_dir, 'dashboard/tree_visualization.png'))
    plt.close(fig)
