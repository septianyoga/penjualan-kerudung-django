import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt
from prediction.models import ProcessingDataLatih
import os

# Fungsi untuk melatih model
def train_model():
    # Query data from ProcessingDataLatih model
    data_latih = ProcessingDataLatih.objects.all()

    # Convert the query set to a list of dictionaries
    data_list = list(data_latih.values('brand', 'jenis', 'bahan', 'harga', 'ukuran_kain', 'terjual'))

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    # Check for missing values and handle them
    df = df.dropna()  # Drop rows with any missing values

    # Ensure 'terjual' is correctly mapped to 'yes' or 'no'
    df['terjual'] = df['terjual'].map({1: 'yes', 0: 'no'})  # Assuming '1' means 'yes' and '0' means 'no'
    
    # Encode categorical variables
    df_encoded = pd.get_dummies(df[['brand', 'jenis', 'bahan', 'harga', 'ukuran_kain']])
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
    df_input_encoded = df_input_encoded.reindex(columns=feature_columns, fill_value=0)
    prediction = model.predict(df_input_encoded)
    return 'laku tinggi' if prediction[0] == 'yes' else 'laku rendah'

# Fungsi untuk visualisasi pohon keputusan
def plot_tree(model, feature_names, class_names):
    fig = plt.figure(figsize=(10, 8))
    _ = tree.plot_tree(model, feature_names=feature_names, class_names=class_names, filled=True)
    # Simpan gambar di folder static
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    plt.savefig(os.path.join(static_dir, 'tree_visualization.png'))
    plt.close(fig)
