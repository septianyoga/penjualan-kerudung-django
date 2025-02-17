"""
URL configuration for penjualan_kerudung project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from landingpage.views import landing_page
from dashboard.views import dashboard_view, kelola_data, preprocessing, models, performance, processing_data_v

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', landing_page, name='landing_page'),
    path('', lambda request: redirect('dashboard',
         permanent=True), name='dashboard'),
    path('login/', include('authentication.urls')),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('kelola-data', kelola_data, name='kelola_data'),
    path('preprocessing', preprocessing, name='preprocessing'),
    path('processing-data', processing_data_v, name='processing_data'),
    path('models', models, name='models'),
    path('performance', performance, name='performance'),

]
