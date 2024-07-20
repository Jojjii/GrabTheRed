import cv2
import numpy as np
from funcs import detHand
import pyautogui as pag

cam = cv2.VideoCapture(0)

lower = np.array([155,50,0])  #bounds for red color
upper = np.array([179,255,255])

oldX = 0

while True:
    nouse, frame = cam.read()
    
    countours, nouse = detHand(frame,lower,upper)


    for c in countours:
        area = cv2.contourArea(c)
        if(area>1000):
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        
            
            if x > oldX:
                pag.press('a')
            
            if x < oldX:
                pag.press('d')
            
            oldX = x


            
    cv2.imshow("Move The Car",frame)
            

    key = cv2.waitKeyEx(1) 
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()