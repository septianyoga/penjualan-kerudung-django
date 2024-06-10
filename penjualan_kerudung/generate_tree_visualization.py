from prediction.ml_model import train_model, plot_tree

# Latih model dan buat visualisasi pohon keputusan
model, feature_columns = train_model()
plot_tree(model, feature_columns, model.classes_)
