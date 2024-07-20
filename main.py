import pygame
import cv2
import numpy as np
import math as m
import time
import pyautogui as pag
from funcs import scale,  imgRot, detHand




pygame.font.init()


def calcDis(p1, p2):
    if(p1 and p2):
        return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    
    return 1


GRASS = scale(pygame.image.load("grass.jpg"),3)
TRACK = scale(pygame.image.load("track.png"),1.1)
BORDER = scale(pygame.image.load("border.png"),1.1)
FINISH = scale(pygame.image.load("finish.png"),0.9)
FLAG = scale(pygame.image.load("flg.png"),0.5)
flag_width, flag_height = FLAG.get_width(), FLAG.get_height()
flagMask =   pygame.mask.from_surface(FLAG)

purpleCar =scale( pygame.image.load("purple-car.png"),0.7)
redCar = scale(pygame.image.load("red-car.png"),0.7)

borderMask = pygame.mask.from_surface(BORDER)

width, height = TRACK.get_width(), TRACK.get_height()
win= pygame.display.set_mode((width, height))
pygame.display.set_caption("GrabTheRed")

font = pygame.font.SysFont("comicsans",30) 

cam = cv2.VideoCapture(0)

lower = np.array([155,50,0])  #bounds for red color
upper = np.array([179,255,255])

oldX = 0

oldY = 0

class car:
  
  
    def __init__(self,maxV, rotV):
        self.img = self.IMG
        self.maxV = 10
        self.velocity = 0
        self.rotV = rotV
        self.angle = 0 
        self.x, self.y = self.START_POS
        self.acc = 0.1

    def rot(self,left=False, right=False):
        if left:
            self.angle += self.rotV
        elif right:
            self.angle -= self.rotV

        
    def d(self,win):
        imgRot(win,self.img,(self.x,self.y),self.angle)
    
    def driveFwd(self):
            self.velocity = min(self.velocity + self.acc, self.maxV)
            self.drive()

    def drive(self):
        rad = m.radians(self.angle)
        vert = m.cos(rad) * self.velocity
        horiz = m.sin(rad) * self.velocity
        self.x -= horiz
        self.y -= vert
    
    def driveBckwd(self):
        self.velocity = max (self.velocity - self.acc, -self.maxV)
        self.drive()

    def slowDown(self):
        self.velocity = max(self.velocity-(self.acc)/2,0)
        self.drive()
    
    def collision(self, callingMask, x=0, y=0):
        carMask = pygame.mask.from_surface(self.img)
        offset = (int(self.x),int(self.y))
        calc = callingMask.overlap(carMask,offset)

        return calc
    
    def thirdLaw(self):
        self.velocity = -(self.velocity)/1.5
        self.drive()

    def ctf(self, flags, fcount):
        car_rect = self.img.get_rect(topleft=(int(self.x), int(self.y)))

        for flag_pos in flags:
            flag_rect = pygame.Rect(flag_pos[0], flag_pos[1], flag_width, flag_height)
            if car_rect.colliderect(flag_rect):
                flags.remove(flag_pos)
                return flags, fcount + 1

        return flags, fcount

    def getv(self):
        return self.velocity
    
class mainCar(car):
    IMG = redCar
    START_POS = (180,200)

def draw(win,imgs,flags,pc):
    for pic,pos in imgs:
        win.blit(pic,pos)
    pc.d(win)
    for pos in flags:
        win.blit(FLAG,pos)
    
    flag_text = font.render(f'Flag Captured: {fcount}', True, (0, 0, 0))
    win.blit(flag_text, (10, height - 100))
    v = player.getv()
    speed_text = font.render(f'Speed: {round(v)}', True, (0, 0, 0))
    win.blit(speed_text, (10, height - 50))
  
    pygame.display.update()


fps = 60
clk = pygame.time.Clock()
player = mainCar(6,5)
run = True

imgs = [(GRASS,(0,0)),(TRACK,(0,0)),(BORDER,(0,0)),(FINISH,(170,200))]
        
flags = [(70,200),(200,700),(400, 850),(800,850),(800,400),(800,50)]
fcount = 0

# lower = np.array([165,0,0])
# upper = np.array([179,150,150])
prev_y = 0
prev_x = 0

lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
lower_red2 = np.array([165, 0, 0])
upper_red2 = np.array([180, 255, 255])


threshRight = 0.3
threshLeft = 0.7
cam = cv2.VideoCapture(0)

while run:

  clk.tick(fps)
  
  flag = False

  draw(win,imgs,flags,player)
 
  nouse, frame = cam.read()
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


  mask1 = cv2.inRange(hsv, lower_red, upper_red)
  mask2 = cv2.inRange(hsv, lower_red2, upper_red2)


  mask = cv2.bitwise_or(mask1, mask2)

#   mask = cv2.inRange(hsv, lower, upper)


  contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
  text = "Driving Forward"

  contflag = False
  for c in contours:
        if (contflag):
            break
        area = cv2.contourArea(c)
        if area > 5000:
            
            contflag = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            dist = x-prev_x
            # fdist = y-prev_y
            
            if x > prev_x:
                player.rot(left=True)
                text = "Steering Left"

            elif x < prev_x:

                player.rot(right=True)
                text = "Steering Right"
            
            elif y > prev_y:

                flag = True
                player.driveBckwd()
                text = "Driving Backwards"
            
            
            if flag is False:
                # player.slowDown()
                player.driveFwd()
            

            prev_x  = x                
            prev_y  = y

            flag = False
        


  if cv2.waitKey(5) == ord('q'):
        break
  
  flags, fcount = player.ctf(flags,fcount)
  
  cv2.putText(frame, text, (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


  cv2.imshow("Demo", frame)

  pygame.display.flip()


  coll = False
  draw(win,imgs,flags,player)

  if player.collision(borderMask) and coll == False:
      player.thirdLaw()
      coll = True
  elif player.collision(borderMask) and coll == True:
      coll = False

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      break
        

pygame.quit()