import cv2

cap = cv2.VideoCapture(0)  #for capturing image. Basically the source of the image
while cap.isOpened():
    ret, back = cap.read() #reading from the camera/webcam
    # ret will acknowledge whether the camera is working or not. True or False
    #back stores whatever the camera is reading.
    if ret:
        cv2.imshow("image",back) # showing the image
        if cv2.waitKey(5)==ord('q'): #save the image. ord('q') gives the unicode value of q. The
            #waitKey(5) will wait for 5 sec and if in b/w we press any key, then it will compare
            #it with ord('q') and follow the steps mentioned like saving the image.
            cv2.imwrite('image.jpg',back)
            break
cap.release() #release all resources
cv2.destroyAllWindows()
