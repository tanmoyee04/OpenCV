# -*- coding: utf-8 -*-
"""
Created on Mon May 24 09:38:35 2021

@author: Tanmoyee
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
back = cv2.imread('./image.jpg')

while cap.isOpened(): #take each frame
    ret, frame = cap.read() #frame is what the camera is reading
    if ret:
        #we will be using hsv instead of rgb because hsv is the combination is primary colors
        #along with light, intensity, etc. Basically it is the color which the human eye sees.
        #Whereas rgb is the combination of primary colors. Thus we need to convert rgb to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #cv2.imshow("hsv",hsv)
        #now calculate the value of hsv.
        #lower: hue-10,100,100 and higher: hue+10,255,255
        blue = np.uint8([[[0,0,255]]]) #BGR values 
        hsv_blue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV) #get HSV value of blue from BGR
        print(hsv_blue) # I have converted blue because my cloak color is blue
        
        #threshold the hsv value to get only blue colour
        l_blue = np.array([94, 80, 2])
        u_blue = np.array([126, 255, 255])
        
        mask = cv2.inRange(hsv,l_blue,u_blue)
        #cv2.imshow("mask",mask)
        #part1: all the blue things
        part1 = cv2.bitwise_and(back,back,mask=mask) # The bitwise_and is replacing all the blue
        #colored pixels with the background image that was captured earlier.
        #cv2.imshow("part1",part1)
        
        mask = cv2.bitwise_not(mask)
        
        #part2: all the not blue things
        part2 = cv2.bitwise_and(frame,frame,mask=mask)
        #cv2.imshow("mask",part2)
        
        #We wanna show both part1+part2
        cv2.imshow("cloak",part1+part2)
        
        
        if cv2.waitKey(5)==ord('q'):
            break
        
cap.release() #release all resources
cv2.destroyAllWindows()