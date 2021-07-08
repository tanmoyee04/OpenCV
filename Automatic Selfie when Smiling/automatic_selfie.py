# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 15:34:22 2021

@author: USER
"""

import cv2
import datetime

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

while True:
    _, frame = cap.read()
    original_frame = frame.copy() #copying the frame
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Converting to grey scale
    face = face_cascade.detectMultiScale(gray,1.3,5) #1.3 is the scale and 5 is how big we want to detect
    
    #for drawing a rectangle arround the face
    for X, Y, W, H in face:
        cv2.rectangle(frame, (X,Y), (X+W,Y+H), (0,255,255))
        
        #For detecting the smile, te smile has to be inside the rectangle. Thus we will be declairing a Region of Interest
        face_roi = frame[Y:Y+H,X:X+W]
        
        #But for detecting, we need to use grayscale
        gray_roi = gray[Y:Y+H,X:X+W]
        
        smile = smile_cascade.detectMultiScale(gray_roi,1.3,25) #detected the smile
        
        #for the smile, we again have to draw a rectangle.
        for X1, Y1, W1, H1 in smile:
            cv2.rectangle(face_roi, (X1,Y1), (X1+W1,Y1+H1), (0,0,255),2)
            
            time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            file_name = f'selfie-{time_stamp}.png' #dynamic file name
            
            # Final step is to save the image in the form of selfie
            cv2.imwrite(file_name, original_frame) # Since we don't want pictures with boders
    
    cv2.imshow("Image",frame)
    if cv2.waitKey(10) == ord('q'):
        break
