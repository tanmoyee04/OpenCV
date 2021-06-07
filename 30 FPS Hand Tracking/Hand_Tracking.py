'''hand tracking uses two main modules at the backend : palm detection and hand landmarks
Palm detection works on the complete image and from there it crops the image of the hand
From there hand landmark module finds 21 different landmarks from the cropped image of the hand

In this project I will be using mediapipe package. MediaPipe offers open source cross-platform, 
customizable ML solutions for live and streaming media. e.g: face mesh, human pose detection,
hand tracking, object detection & tracking, etc'''

import cv2
import mediapipe as mp


mpHands = mp.solutions.hands #importing func named hands
Hands = mpHands.Hands() #saving the fun in a variable named Hands

mpDraw = mp.solutions.drawing_utils #for drawing the lines and points on hand(s)

cap = cv2.VideoCapture(0) #capture video from the camera/webcam



while(cap.isOpened()):
    success, img = cap.read() #provides the frame
    
    converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converting the BGR image to RGB since mediapipe works on RGB images
    results = Hands.process(converted_img) # Processing Image for Tracking
    
    #there can be posibilities that there will be no hands in the frame or can be one or more than one hands in the frame
    if results.multi_hand_landmarks:
        #for hand(s) present in the frame
        for hand_in_frame in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,hand_in_frame,mpHands.HAND_CONNECTIONS) #tracking the dots on the hand(s)
    #to run the webcam
    cv2.imshow("Hand Tracking 30 FPS",img)
    w = cv2.waitKey(1)
    if w==ord('q'): #If the user wants ro quit the game by pressing q
        break
