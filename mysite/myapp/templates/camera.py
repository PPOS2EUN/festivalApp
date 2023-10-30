#!/usr/bin/env python3

import numpy as np
import os
import cv2

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def detect(gray,frame):
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5,minSize=(100,100),flags=cv2.CASCADE_SCALE_IMAGE)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        face_gray = gray[y:y+h,x:x+w]
        face_color = frame[y:y+h,x:x+w]
    return frame


if __name__ == "__main__":
    # Execute when the module is not initialized from an import statement.

    url = 'http://10.32.21.147:4747/video?640x480'

    video_capture = cv2.VideoCapture(url)

    while(True):
        ret, frame = video_capture.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = detect(gray, frame)
        cv2.imshow('video', frame)
        cv2.waitKey(1)

    video_capture.release()
    cv2.destroyAllWindows()
