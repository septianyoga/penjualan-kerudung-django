from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def dashboard_view(request):
    return render(request, 'dashboard/index.html')


@login_required
def kelola_data(request):
    return render(request, 'kelola_data/index.html')

@login_required
def preprocessing(request):
    return render(request, 'preprocessing/index.html')
@login_required
def models(request):
    return render(request, 'model/index.html')

@login_required
def performance(request):
    return render(request, 'performance/index.html')
