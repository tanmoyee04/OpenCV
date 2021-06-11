import cv2
import time
import numpy as np
import Hand_Tracking_Module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

'''Dimension of webcam: 
    wcam = 640
    hcam = 480'''
    
wcam = 640
hcam = 480    

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime = 0

volBar = 350 #for the volume bar
vol = 0
volPer = 0 #for showing the volume percentage

#object creation
detector = htm.handDetector(detectionCon=0.7) #detectioncon is mde to 0.7 to make sure that it is a hand or not

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minvol = volRange[0] #-65.25 
maxvol = volRange[1] #0.0 



while True:
    success, img = cap.read()
    
    #find hand
    img = detector.findHands(img)
    
    #getting the position
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8]) #4 is for tip of thumb and 8 is for tip of index finger
        
        #in order to be sure, I'll make a circle arround the tips
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2 #center of the line
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED) #15 is the radius of the circle
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED) #(x1,y1) and (x2,y2) are centers
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        
        #finding the length of the line i.e the distance b/w the tips
        length = math.hypot(x2-x1,y2-y1)
        #print(length)
        
        #hand range : 50 - 250
        #volume range : -65 - 0
        #we need to convert hand range to volume range using numpy
        vol = np.interp(length,[50,250],[minvol,maxvol])
        volBar = np.interp(length,[50,250],[400,150]) #for the volume bar
        volPer = np.interp(length,[50,250],[0,100]) #for showing the volume percentage on the bar
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
        
        #creating a line between the tips
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        
    #creating rectangle to show the change in volume on the screen withount opening the system's volume panel
    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3) #starting position: (50,150) ending position: (85,400). This is the border for the volume bar
    cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED) #for showing the volume changes
    cv2.putText(img,f'{int(volPer)}%',(40,450),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
    
    #frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    #put the fps on image
    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
    
    cv2.imshow("Image",img)
    w = cv2.waitKey(1)
    if w==ord('q'): #If the user wants ro quit the game by pressing q
        break
