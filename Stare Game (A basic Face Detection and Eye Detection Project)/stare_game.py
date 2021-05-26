''' Basic Face Detection and Eye Detection project'''

import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #for detecting the face 
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml') #for detecting the eyes

first_read = True

cap = cv2.VideoCapture(0) #capture video from the camera/webcam
ret,image = cap.read()

while(ret):
    ret,image = cap.read()
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray,5,1,1) #bilateralfilter is used to remove the impurities 
    #in the harcascade file. Due to the presence of impurities, Harcascade preformes poorly.
    faces = face_cascade.detectMultiScale(gray,1.3,5,minSize=(200,200)) # It searches for the 
    #face frame and keeps on reducing the frame size so that face detection becomes proper and
    #accurate. minsize=(200,200) is the min frame size.
    
    if(len(faces)>0): #This for loop is for all the faces enclosed within the rectangles
        for x,y,w,h in faces:
            image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,225,0),2) #Draws rectangles arround 
            #the face to detect it
            roi_face = gray[y:y+h,x:x+w] #Collects the datapoint from the gray scale image
            roi_face_clr = image[y:y+h,x:x+w] #Collects the datapoint from the coloured image
            eye = eye_cascade.detectMultiScale(roi_face,1.3,5,minSize=(50,50)) #To detect the
            #smaller regions in the face life near the eyes, nose, etc.
            
            #Main game logic
            
            if(len(eye)>=2): #If it detects more than two eyes due to framing
                if(first_read): #If the player has not yet started the game
                    cv2.putText(image,"Press s to begin the game. You blink, you lose!",(100,100),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)
                else:
                    print("*****************************************")
            else: 
                if(first_read): #If the game is not running
                    cv2.putText(image,"No eyes are detected!",(100,100),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)
                else: #If the game is running
                    print("Ahhh!!!! You blinked. You lost!")
                    first_read = True
    else:
        cv2.putText(image,"No face is detected. Try again.",(100,100),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2) #If no face is detected by the system.
            
    cv2.imshow('image',image)
    w = cv2.waitKey(1)
    if w==ord('q'): #If the user wants ro quit the game by pressing q
        break
    elif(w==ord('s') and first_read): #If the user wants to start the game by pressing s
        first_read = False
            
cap.release()
cv2.destroyAllWindows()
