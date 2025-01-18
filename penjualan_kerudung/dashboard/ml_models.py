import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from .models import ProcessingDataLatih
import matplotlib.pyplot as plt
import os

# Fungsi untuk melatih model


def train_model():
    # Data baru dari gambar
    # data = {
    #     'brand': ['A', 'A', 'B', 'C', 'C', 'C', 'B', 'A', 'A', 'C', 'A', 'B', 'B', 'C'],
    #     'jenis': ['t-shirt', 't-shirt', 'dress', 'pants', 'skirt', 'skirt', 'dress', 'pants', 't-shirt', 'pants', 't-shirt', 'dress', 't-shirt', 'skirt'],
    #     'bahan': ['cotton', 'cotton', 'silk', 'denim', 'polyester', 'polyester', 'silk', 'denim', 'cotton', 'denim', 'cotton', 'silk', 'cotton', 'polyester'],
    #     'harga': ['high', 'high', 'low', 'medium', 'medium', 'high', 'low', 'medium', 'medium', 'medium', 'low', 'medium', 'low', 'high'],
    #     'ukuran_kain': ['S', 'S', 'M', 'M', 'L', 'L', 'XL', 'M', 'S', 'L', 'M', 'XL', 'L', 'M'],
    #     'terjual': ['no', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'no']
    # }
    data = ProcessingDataLatih.objects.all().values('brand', 'jenis', 'bahan', 'harga', 'ukuran_kain', 'terjual')

    df = pd.DataFrame(data)

    # Encode categorical variables
    df_encoded = pd.get_dummies(
        df[['brand', 'jenis', 'bahan', 'harga', 'ukuran_kain']])
    X = df_encoded
    y = df['terjual']

    # Training decision tree
    clf = DecisionTreeClassifier(criterion='entropy')
    clf = clf.fit(X, y)

    return clf, X.columns

# Fungsi untuk prediksi


def predict_sales(model, feature_columns, input_data):
    df_input = pd.DataFrame([input_data])
    df_input_encoded = pd.get_dummies(df_input)
    df_input_encoded = df_input_encoded.reindex(
        columns=feature_columns, fill_value=0)
    prediction = model.predict(df_input_encoded)
    return prediction[0]

# Fungsi untuk visualisasi pohon keputusan


def plot_tree(model, feature_names, class_names):
    fig = plt.figure(figsize=(20, 10)) 
    _ = tree.plot_tree(model, feature_names=feature_names, class_names=class_names,
    filled=True, rounded=True, fontsize=10) 

    # Simpan gambar di folder static
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    plt.savefig(os.path.join(static_dir, 'dashboard/tree_visualization.png'))
    plt.close(fig)
