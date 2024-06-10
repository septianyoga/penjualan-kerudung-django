import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt
import os

# Fungsi untuk melatih model


def train_model():
    # Data baru dari gambar
    data = {
        'outlook': ['sunny', 'sunny', 'cloudy', 'rainy', 'rainy', 'rainy', 'cloudy', 'sunny', 'sunny', 'rainy', 'sunny', 'cloudy', 'cloudy', 'rainy'],
        'temperature': ['hot', 'hot', 'hot', 'mild', 'cool', 'cool', 'col', 'mild', 'co', 'mild', 'mild', 'mild', 'hot', 'mild'],
        'humidity': ['high', 'high', 'high', 'high', 'normal', 'normal', 'normal', 'high', 'normal', 'normal', 'normal', 'high', 'normal', 'high'],
        'windy': [False, True, False, False, False, True, True, False, False, False, True, True, False, True],
        'play': ['no', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'no']
    }

    df = pd.DataFrame(data)

    # Encode categorical variables
    df_encoded = pd.get_dummies(
        df[['outlook', 'temperature', 'humidity', 'windy']])
    X = df_encoded
    y = df['play']

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
    fig = plt.figure(figsize=(10, 8))
    _ = tree.plot_tree(model, feature_names=feature_names,
                       class_names=class_names, filled=True)
    # Simpan gambar di folder static
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    plt.savefig(os.path.join(static_dir, 'tree_visualization.png'))
    plt.close(fig)
