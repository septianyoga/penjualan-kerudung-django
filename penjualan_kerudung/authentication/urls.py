from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_v, name='login'),
    path('logout', views.logout_v, name='logout'),
]
