from django.http import HttpResponse
from django.template import loader
import cv2
import asyncio
import json
import websockets

def faceRecognize(request):
  template = loader.get_template('faceRecognize.html')
  return HttpResponse(template.render())


def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())



def form(request):
  template = loader.get_template('form.html')
  return HttpResponse(template.render())


def welcome(request):
  template = loader.get_template('welcome.html')
  return HttpResponse(template.render())