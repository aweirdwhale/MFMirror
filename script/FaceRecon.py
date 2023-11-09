#pip install opencv-python 
import os
import cv2

os.getcwd()
face_cascade = cv2.CascadeClassifier('./config/face_detector.xml')
img = cv2.VideoCapture(0)

faces = face_cascade.detectMultiScale(img,1.1, 4)

for (x, y , w, h) in faces:
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,255), 2)
    cv2.imwrite("face_detected.png", img)
    print("enregistré avec succès")