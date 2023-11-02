from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('faceDet/', views.faceDet, name='faceDet'),
    path('detectme',views.detectme,name='detectme'),
    path('detectface',views.detectface,name='detectface'),
#    path('Form',views.Form ,name='Form')
    ]
