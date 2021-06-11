# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 19:01:11 2021

@author: Tanmoyee
"""

import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands #importing func named hands
        self.Hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon) #saving the fun in a variable named Hands
        self.mpDraw = mp.solutions.drawing_utils #for drawing the lines and points on hand(s)

    def findHands(self,img,draw=True):
        converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converting the BGR image to RGB since mediapipe works on RGB images
        self.results = self.Hands.process(converted_img) # Processing Image for Tracking
    
        #there can be posibilities that there will be no hands in the frame or can be one or more than one hands in the frame
        if self.results.multi_hand_landmarks:
            #for hand(s) present in the frame
            for hand_in_frame in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,hand_in_frame,self.mpHands.HAND_CONNECTIONS) #tracking the dots on the hand(s)
        return img
    
    def findPosition(self,img,handNo=0,draw=True):
        lmList=[] #landmark list which will have all the positions
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo] #get the elements of the first hand
            for id,lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h) #center
                    #print(id, cx, cy)
                    lmList.append([id, cx, cy])
                    #if id==0: #first landmark generally at the bottom of the palm then draw the circle
                    if draw:
                        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED) #15 is the radius of the circle. (255,0,255) is for purple color
        
        return lmList
def main():
    ptime=0 #previous time
    ctime=0 #current time
    cap = cv2.VideoCapture(0) #capture video from the camera/webcam
    
    detector = handDetector() #object

    while(cap.isOpened()):
        success, img = cap.read() #provides the frame
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[4]) #landmark 4 is for tip of the thumb finger
        ctime = time.time()
        fps = 1/(ctime - ptime)
        ptime = ctime
    
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    
        #to run the webcam
    
        cv2.imshow("Hand Tracking 30 FPS",img)
        w = cv2.waitKey(1)
        if w==ord('q'): #If the user wants ro quit the game by pressing q
            break
    
    
if __name__ == "__main__":
    main()