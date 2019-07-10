import cv2
import numpy as np
from point import point
from path import path

from math import sqrt,sin,cos, asin


class demoRobot:    
    def __init__(self):
        self.dphi=0;
        self.v=point(1,0);
        self.p=point(40,40);
        self.phi=0;
    def comp_dphi(self,p):
        dphi_,err=self.v.getAngle(p-self.p)
        if(err==0):
            self.dphi=dphi_
    def go(self,targ):
#        print(self.p.vecF())
        
        self.p+=(self.v*4);
        
        self.comp_dphi(targ)
        if((self.p-targ).length2()>100):
            self.phi+=self.dphi*0.07;
        
        self.v=point(cos(self.phi),sin(self.phi));

DR=demoRobot();

      
x_=np.array([100,200,300,400,500,550,560])
#y_=np.array([100,200,100,100,100,100,100])
y_=np.array([100,110,80,120,140,180,200])
pioneerPath=path(x_,y_)
pioneerPath.comp_n()
targ=point(10,10)   


def max(a,b):
    if a>b:
        return a
    else:
        return b
    
def min(a,b):
    if a<b:
        return a
    else:
        return b
    
    
cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('window')

# Starting with 100 to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'window',0,179,nothing)
h = cv2.setTrackbarPos('h','window', 116)
cv2.createTrackbar('s', 'window',0,255,nothing)
h = cv2.setTrackbarPos('s','window', 159)
cv2.createTrackbar('v', 'window',0,255,nothing)




size = 480, 640, 3
result_ac=np.zeros(size, dtype=np.uint8)
write_on=0;
wind=20;

if write_on:
    out = cv2.VideoWriter('hsv_.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 24, (640,480))

def click_and_crop(event, x, y, flags, DR):
    if(event==cv2.EVENT_LBUTTONDOWN):
        p=point(x,y)
        global targ
        targ=p
#        print(DR.p.vec())
#        targ=p
#        print(targ.vec())
#        print(pioneerPath.is_right(p,0))
#        print(DR.v.getAngle(p-DR.p))
        
cv2.setMouseCallback("window", click_and_crop)
#print(pioneerPath.p);

while(1):

    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','window')
    s = cv2.getTrackbarPos('s','window')
    v = cv2.getTrackbarPos('v','window')



    # Normal masking algorithm
    
#    wind=v;
    k=0.15;
#    upper_blue = np.array([180,255,255])
#    upper_blue = np.array([thresh(h+wind,180),thresh(s+wind,255),thresh(v.+wind,255)])
    lower_blue1 = np.array([h,s,v])
    upper_blue1 = np.array([min(179,h+wind),255,255])
    
#    lower_blue2 = np.array([h,s,v])
    upper_blue2 = np.array([max(-1,h+wind-180),255,255])

    mask = cv2.inRange(hsv,lower_blue1, upper_blue1)
    mask_h= cv2.inRange(hsv,np.array([0,0,0]), upper_blue2)
    mask|=mask_h
#    mask=mask_h
#    mask=~mask

    result = cv2.bitwise_and(frame,frame,mask = mask)
#    result=cv2.blur(result,(10,10))
#    result_ac=cv2.addWeighted(result,k,result_ac,1-k,0)
   # calculate moments of binary image
   
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    M=cv2.moments(gray)
#    print(M["m00"])
# calculate x,y coordinate of center
    if(M["m00"]!=0):
        cX = int(M["m10"] / M["m00"]) 
        cY = int(M["m01"] / M["m00"])
        cv2.circle(result, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(result, "centroid", (cX - 25, cY - 40),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    else:
        cX=640;
        cY=480;
#    print(pioneerPath.i)
    pioneerPath.check_reached(DR.p);
    DR.go(pioneerPath.pt);
#    if()
#    print(pioneerPath.is_right(DR.p,0))
#    print(targ.vec())
    cv2.circle(result, DR.p.vec(), 6, (255, 0, 255), -1)
    cv2.circle(result, pioneerPath.pt.vec(), 5, (0, 255, 255), -1)
    
    result=pioneerPath.draw(result)
#    print(pioneerPath.size)
    cv2.imshow('window',result)

    
    
    
    if write_on:
        out.write(result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        if write_on:
            out.release()
        break

cap.release()

cv2.destroyAllWindows()