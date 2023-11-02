from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import os, sys
import Jetson.GPIO as GPIO
from time import sleep
from queue import Queue
import face_recognition
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/8


droidCam_url = 'https://192.168.0.10:4343/video'
isCenter = False

global DIR, STEP

DIR = 10
STEP = 8
CW = 1
CCW = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, GPIO.HIGH)

def home(request):
    host = request.get_host()  # This will get the host:port
    context = {
        'host': host
    }

    return render(request, "home.html",context)

def Form(request, isTrue):
    if isTrue:
        return render(request, "Form.html")

class VideoCamera(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VideoCamera, cls).__new__(cls)
            cam = cv2.VideoCapture(droidCam_url)
            #cam.set(3, 640)
            #cam.set(4, 480)
            cls._instance.video = cam
            (cls._instance.grabbed, cls._instance.frame) = cls._instance.video.read()
            threading.Thread(target=cls._instance.update, args=()).start()
        return cls._instance

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        center = None

        if image is None or image.size == 0:
            return None, None
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	## face_recognition ##
        #cv2.imshow("gray",gray)
        #cv2.waitKey(1)
        #rgb_small_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #face_locations = face_recognition.face_locations(rgb_small_frame)
        print(face_locations)
        faces = face_cascade.detectMultiScale(gray,1.3, 5)
        #print("shape",image.shape)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)
            center = (y+y+h)/2
            #SetStepDirection(center)
	    
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        _, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes(), center

    def get_face_detected_frame(self):
        image = self.frame
        if image is None or image.size == 0:
            return None
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def SetStepDirection(centerROI):
    # CCW => UPUPUPUPUPP
    # CW => DOWN
    #print("centerRoI",centerROI)
    #print("centerTopPoint",centerTopPoint)
    if 300 <= centerROI and centerROI <= 340:
        print("============center============")
        return "center"
    elif 340 < centerROI and centerROI < 640:
        GPIO.output(DIR, CW)
        #print('\33[31m', "sd",'\33[0m',)
        print("sd")
        return "CW"
    elif 0 < centerROI and centerROI < 300:
        GPIO.output(DIR, CCW)
        print('\33[31m', "sd2",'\33[0m',)
        return "CCW"

class StepMotorThread(threading.Thread):
    def __init__(self, command_queue):
        threading.Thread.__init__(self)
        self.command_queue = command_queue
        self.daemon = True
        self.start()

    def run(self):
        while True:
            command = self.command_queue.get()
            if command == "CW" or command == "CCW":
                GPIO.output(DIR, CW if command == "CW" else CCW)
                for _ in range(100):
                    GPIO.output(STEP, GPIO.HIGH)
                    sleep(.0005)
                    GPIO.output(STEP, GPIO.LOW)
                    sleep(.0005)
                self.command_queue.task_done()

command_queue = Queue()
step_motor_thread = StepMotorThread(command_queue)
def gen(camera):
    while True:
        frame, center = camera.get_frame()
        print(isCenter)

        if frame is not None:
            if center is not None and command_queue.empty():
                print(center)
                command = SetStepDirection(center)
                if command in ["CW", "CCW"]:
                    command_queue.put(command)
                elif "center":
                    isCenter = True
                    Form(isCenter)
                    print(isCenter)
                #sleep(1.0)
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_face_detected(camera):
    while True:
        frame = camera.get_face_detected_frame()
        if frame is not None:
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def rec(self):
    cv2.imshow("gray",gray)
    cv2.waitKey(1)
    rgb_small_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)

@gzip.gzip_page
def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass

@gzip.gzip_page
def detectface(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen_face_detected(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # Better to handle specific exceptions
        print("에러입니다...")
        pass


