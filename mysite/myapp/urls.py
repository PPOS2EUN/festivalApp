from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    path('face/', views.faceRecognize, name='faceRecognize'),
    path('form/', views.form, name='form'),
]