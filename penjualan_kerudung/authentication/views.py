from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

# Fungsi pengujian untuk memeriksa apakah pengguna belum diautentikasi


def user_not_authenticated(user):
    return not user.is_authenticated


@user_passes_test(user_not_authenticated, login_url='dashboard')
def login_v(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Lakukan validasi input
        if not username or not password:
            return render(request, 'auth/login.html', {'error': 'Please enter both username and password'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid username or password'})
    return render(request, 'auth/login.html')


def logout_v(request):
    logout(request)
    return redirect('login')
