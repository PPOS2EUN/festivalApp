from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import threading
import os, sys
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/8
import face_recognition
import cv2
import numpy as np

import sys
import argparse
# import Jetson.GPIO as GPIO
from time import sleep


droidCam_url = 'https://10.32.21.71:4343/video'

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# todo FACE DETECTION
def home(request):
    host = request.get_host()  # This will get the host:port
    context = {
        'host': host
    }
    return render(request, "home.html", context)

def Form(request):
    return render(request, "Form.html")
class VideoCamera(object):
    _instance = None

    def __new__(cls):
      if cls._instance is None:
        cls._instance = super(VideoCamera, cls).__new__(cls)
        cls._instance.video = cv2.VideoCapture(droidCam_url)
        (cls._instance.grabbed, cls._instance.frame) = cls._instance.video.read()
        threading.Thread(target=cls._instance.update, args=()).start()
      return cls._instance

    def __del__(self):
      self.video.release()

    def get_frame(self):
      image = self.frame
      if image is None or image.size == 0:
        return None
      _, jpeg = cv2.imencode('.jpg', image)
      return jpeg.tobytes()


    def get_face_detected_frame(self):
        image = self.frame
        if image is None or image.size == 0:
            return None
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def update(self):
      while True:
        (self.grabbed, self.frame) = self.video.read()

def gen(camera):
  while True:
    frame = camera.get_frame()
    if frame is not None:
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen_face_detected(camera):
  while True:
    frame = camera.get_face_detected_frame()
    if frame is not None:
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @gzip.gzip_page
# def detectme(request):
#     try:
#         cam = VideoCamera()
#         return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
#     except:  # This is bad! replace it with proper handling
#         print("error...")
#         pass

@gzip.gzip_page
def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen_face_detected(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # Better to handle specific exceptions
        print("error...")
        pass

#============================================================================================================
#============================================================================================================
# todo MOVING ACTUATOR

# global DIR, STEP
#
# DIR = 10
# STEP = 8
#
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(DIR, GPIO.OUT)
# GPIO.setup(STEP, GPIO.OUT)
# GPIO.output(DIR, GPIO.HIGH)
#
# class step:
#     def __init__(self):
#         self.id = 0
#         self.motor = 0
#         self.centerY = 0
#         self.face_detection(self.id, self.centerY)
#         self.SetStepDirection(self.motor)
#
#     def face_detection(self, id, centerY):
#         # capture the next image
#         img = input.Capture()
#         self.id = id
#         self.centerY = centerY
#
#         for detection in detections:
#             print(detection)
#             print(detection.Center)
#             self.id = detection.ClassID
#             self.centerY = detection.Center[1]
#             print("center x = ", detection.Center[0])
#             print("center y = ", detection.Center[1])
#
#         output.Render(img)
#         output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))
#
#     def SetStepDirection(self, motor):
#         self.motor = motor
#         print(self.centerY, self.id)
#
#         if self.centerY <= 349 and 369 <= self.centerY:
#             print("============center============")
#             return "center"
#         # UP
#         elif 0 < self.centerY and self.centerY < 349:
#             GPIO.output(DIR, GPIO.HIGH)
#             self.motor = self.motor + 1
#             return "CW"
#         # DOWN
#         elif 369 < self.centerY and self.centerY < 719:
#             GPIO.output(DIR, GPIO.LOW)
#             self.motor = self.motor - 1
#             return "CCW"
#         # HOME
#         elif self.motor == 0 or self.motor == 10666:
#             return "HOME"
#
#         print("current motor step:", end=" ")
#         print(self.motor)
#
#
# if __name__ == '__main__':
#     while True:
#         s = step()
#         if not s.SetStepDirection(0) == "CW" or not s.SetStepDirection(0) == "CCW":
#             continue
#         GPIO.output(STEP, GPIO.HIGH)
#         sleep(.005)
#         GPIO.output(STEP, GPIO.LOW)
#
#         if not :
#             GPIO.cleanup()
#             break