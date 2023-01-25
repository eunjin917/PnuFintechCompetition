"""Fintech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

import Fintechapp.views

urlpatterns = [
    path('admin', admin.site.urls), 
    path('', Fintechapp.views.index, name="index"),  
    path('company_good/c<int:company_pk>/g<int:good_pk>', Fintechapp.views.company_good, name="company_good"), 
    path('setting_data', Fintechapp.views.setting_data, name="setting_data"),  
    path('update', Fintechapp.views.update, name="update"),     
    path('alarm_setting', Fintechapp.views.alarm_setting, name="alarm_setting"),
]