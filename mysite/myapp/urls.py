from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('detectme', views.detectme,name='detectme'),
    path('Welcome', views.Welcome, name='Welcome'),
    path('Form', views.Form, name='Form')
]