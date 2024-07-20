import pygame as pg
import cv2
import numpy as np

def scale(image, fac):
    return pg.transform.scale(image, (round(image.get_width()*fac),round(image.get_height()*fac)))

def imgRot(win,img,topLeft,angle):
    nimg = pg.transform.rotate(img,angle)
    nrect = nimg.get_rect(center=img.get_rect(topleft=topLeft).center)
    win.blit(nimg,nrect.topleft)


def detHand(frame,lower,upper):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)   
    
    return cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  