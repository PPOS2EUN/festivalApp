import cv2
import sys

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 개체가 재대로 생성됬는지 확인
if classifier.empty():
    print('XML load failed!')
    sys.exit()
