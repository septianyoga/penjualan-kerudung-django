from django.shortcuts import render
from .ml_model import train_model, predict_sales, plot_tree

model, feature_columns = train_model()
plot_tree(model, feature_columns, model.classes_)


def predict_view(request):
    prediction = None
    if request.method == 'POST':
        outlook = request.POST.get('outlook')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        windy = request.POST.get('windy') == 'TRUE'
        input_data = {'outlook': outlook, 'temperature': temperature,
                      'humidity': humidity, 'windy': windy}
        prediction = predict_sales(model, feature_columns, input_data)

    return render(request, 'prediction/predict.html', {'prediction': prediction})
