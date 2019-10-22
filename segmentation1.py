import cv2
import numpy as np
#from pyimagesearch import imutils
from point import point
from path import path
from obstacle import obstacle
import socket
from msvcrt import getch
#from statistics import median


UDP_active=False
UDP_active_h=UDP_active
rot_speed_k=26
speed=120#60
IP='169.254.104.146'
PORT=49122
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
UDP_cnt=0
#UDP_active=True
#
x_=np.array([100,200,300,400,500,550,560])
y_=np.array([100,110,80,120,140,180,200])


#x_=np.array([560,550,500,400,300,200,100])
#y_=np.array([200,180,140,120,80,110,100])

y_+=140

time=0

#import copy

from math import sqrt,sin,cos, asin

#function for masks
def pre_median_y(img):
    sums=np.empty(img.shape[0])
    for i in range(0,img.shape[0]):
        sums[i]=(img[i].sum())
    sums=sums.nonzero()[0]
#    print('sum: ',sums)
    out=sorted(range(len(sums)), key=lambda k: sums[k])
#    print(out)
    if(len(out)):
#        return [out[int(len(out)/2)], 0]
        return [out[int(len(out)*0.5)], 0]
    else:
        return [1,1]
    
#    return 1
#    return sums
mY=1
mX=1 
    
    
    
    

class Agent:    
    def __init__(self):
        
        self.dirs_ptr=0;
        self.dirs_cnt=0;
        self.dphi=0;
        self.dirs=[point()]*20;
        self.dir=point(1,0);
        self.p=point(1,0);
        self.p1=point();
        self.phi=0;
    def comp_dphi(self,p):
        dphi_,err=self.v.getAngle(p-self.p)
        if(err!=1):
            self.dphi=dphi_
            
    def setP(self,p):
        self.p=p;    
    def comp_dir(self):
        
#        if((self.p1-self.p).length2()>150):
#            self.dir=self.p-self.p1
#            self.dir.norm()
#            self.p1=self.p
        
        
        
        if(self.dirs_cnt==0):
            self.dirs[self.dirs_ptr]=self.p-self.p1
            self.p1=self.p
            
            self.bb=point()
            for ab in self.dirs:
                self.bb=self.bb+ab
#            print(self.bb.vec())
            dir,err =self.bb.norm()
            
            if(err==0):
                self.dir=dir
            self.dirs_ptr+=1
            if(self.dirs_ptr==len(self.dirs)):
                self.dirs_ptr=0
        
        self.dirs_cnt+=1
        if(self.dirs_cnt==1):
            self.dirs_cnt=0;
            
 
            
        
    def go_(self,targ):
#        print(self.p.vecF())
        
        self.p+=(self.v*4);
        
        self.comp_dphi(targ)
        if((self.p-targ).length2()>100):
            self.phi+=self.dphi*0.07;        
        self.v=point(cos(self.phi),sin(self.phi));

pioneer=Agent();


#y_=np.array([100,200,100,100,100,100,100])
      




pioneerPath=path(x_,y_) #bad __ 
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
cv2.namedWindow('hsv')
cv2.namedWindow('window')

# Starting with 100 to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'window',0,179,nothing)
h = cv2.setTrackbarPos('h','window', 112)

cv2.createTrackbar('s', 'window',0,255,nothing)
s = cv2.setTrackbarPos('s','window', 98)

cv2.createTrackbar('v', 'window',0,255,nothing)
v=cv2.setTrackbarPos('v','window', 189)




size = 480, 640, 3
accumed_img=np.zeros(size, dtype=np.uint8)
write_on=0;
wind=25;

if write_on:
    out = cv2.VideoWriter('hsv_.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 24, (640,480))

def click_and_crop(event, x, y, flags, pioneer):
    if(event==cv2.EVENT_LBUTTONDOWN):
        p=point(x,y)
        global targ,obs_ps,obs,draw_obs
        targ=p
        obs_ps.append(p)
        
        if(len(obs_ps)==4):
            
            obs.createMask(obs_ps);
            obs.createAuxMasks();
            
            draw_obs=1;
            file = open("obstacle.txt","w"); 
            for i in range(0,480):
                for j in range(0,640):
                    file.write(str(obs.mask[i][j])+';'); 
                file.write('\n');
            
        
#        print("hey");
#        print(DR.p.vec())
#        targ=p
#        print(targ.vec())
#        print(pioneerPath.is_right(p,0))
#        print(DR.v.getAngle(p-DR.p))
        
cv2.setMouseCallback("window", click_and_crop)
#print(pioneerPath.p);

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


#pss=[point(233,400),point(300,420), point(200,200)];



    
obs_ps=[];
cX=2;
cY=2;


obs=obstacle();

draw_obs=0;


#file = open("obstacle.txt", "r");
#for i in range(0,480):
#    l=file.readline()[0:1280:2];
#    for j in range(0,640):
#        obs.mask[i,j]=int(l[j]);
#obs.createAuxMasks();   


while(1):
#    if(keyboard.is_pressed('q')):
#        print('hello')
    time+=1
#    print(time)
    _, src_frame = cap.read()
#    cv2.imshow('origin',frame)
    #converting to HSV
    hsv = cv2.cvtColor(src_frame,cv2.COLOR_BGR2HSV)

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
    lower_blue2 = np.array([0,s,v])
    
    upper_blue1 = np.array([min(180,h+wind),255,230])
    upper_blue2 = np.array([max(-1,h+wind-180),255,230])

    kernel = np.ones((7,7),np.float32)/49
    hsv = cv2.filter2D(hsv,-1,kernel)
    mask = cv2.inRange(hsv,lower_blue1, upper_blue1)
    mask_h= cv2.inRange(hsv,lower_blue2, upper_blue2)
    mask|=mask_h
#    mask=mask_h
#    mask=~mask

    masked_img = cv2.bitwise_and(src_frame,src_frame,mask = mask)#whaaaaaaaaaaaaaaaaaaat?????????
#    result=cv2.blur(result,(10,10))
    k=0.9
    accumed_img=cv2.addWeighted(masked_img,k,accumed_img,1-k,0)
   # calculate moments of binary image
#     ..
    result=accumed_img.copy()#for drawing vectors
    gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
   
    
#    edges = cv2.Canny(result,100,200)
#    cnts = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#    cnts = imutils.grab_contours(cnts)
#    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
#    screenCnt = None
#    for c in cnts:
#    	# approximate the contour
#    	peri = cv2.arcLength(c, True)
#    	approx = cv2.approxPolyDP(c, 0.015 * peri, True)
#     
#    	# if our approximated contour has four points, then
#    	# we can assume that we have found our screen
#    	if len(approx) == 4:
#    		screenCnt = approx
#    		break
#    cv2.drawContours(result, [screenCnt], -1, (0, 255, 0), 3)

#___________ALGORYTHM___________     
    
    M=cv2.moments(gray)
    if(M["m00"]!=0):
        cX = int(M["m10"] / M["m00"]) 
        cY = int(M["m01"] / M["m00"])
#    else:
#        cX=640;
#        cY=480;

    pioneerPath.check_reached(pioneer.p);

    
#    mask
#    [mY1,Err1]=pre_median_y(mask)
#    if(not(Err1)):
#        mY=mY1
#    mX=320

    pioneer.setP(point(cX, cY))
    pioneer.comp_dir();
    dphi_,err=(pioneerPath.pt-pioneer.p).getAngle(pioneer.dir)#bad coding is here
    err2=0
    if((pioneerPath.pt-pioneer.p).length2()<900):  
        err2=1
        pioneer.dphi=0
#        print((pioneerPath.pt-pioneer.p).length2())
        
    if((err==0) and (err2==0)):
        pioneer.dphi=dphi_*rot_speed_k
    

    
    
    
    ##_________UDP_time___________
    UDP_cnt+=1;
    rot_speed=0.
    if(UDP_cnt==2):
        UDP_cnt=0
        if(time>40):
            rot_speed=pioneer.dphi
        else:
            rot_speed=0
            
        if(pioneerPath.stop):
            rot_speed=0
            speed=0
#        print(rot_speed)
        if(UDP_active):    
            if(rot_speed<0):
                sock.sendto(bytes([np.uint8(255), np.uint8(rot_speed),1,0]), (IP, PORT))
            else:
                sock.sendto(bytes([0, np.uint8(rot_speed), 1,0]), (IP, PORT))
    if UDP_active_h and not(UDP_active):#            
        sock.sendto(bytes([0,0,0,0]), (IP, PORT))
            
    UDP_active_h=UDP_active
    cv2.line(result,pioneer.p.vec(),(pioneer.p+(pioneer.dir*27)).vec(),(0,255,0),2)
#    pioneer.go(pioneerPath.pt);
    
    
#    
    
#    print(pioneerPath.i)
#    cv2.circle(result, (mX, mY), 5, (255, 0, 0), -1)
    draw_frame=src_frame
    cv2.circle(draw_frame, (cX, cY), 5, (255, 255, 255), -1)
    phrase=['HERE WE GO', 'GO GO GO!!','IM COOL ROBOT', 'YEAH']
#    cv2.putText(draw_frame, phrase[min(pioneerPath.i,0)], (cX - 25, cY - 40),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0,100), 1)

#    if()
#    print(pioneerPath.is_right(DR.p,0))
#    print(targ.vec())
    cv2.circle(draw_frame, pioneer.p.vec(), 6, (255, 0, 255), -1)
    cv2.circle(draw_frame, pioneerPath.pt.vec(), 5, (0, 255, 255), -1)
    
    draw_frame=pioneerPath.draw(draw_frame)
#    draw_frame[200][100]=[255,255,255]
    if(draw_obs):
#        draw_frame = obs.draw(draw_frame)
        draw_frame = cv2.bitwise_and(draw_frame,draw_frame,mask = obs.not_mask)
        draw_frame=draw_frame+obs.blue_mask;
#        cv2.imshow('hsv',obs.blue_mask)
#    print(pioneerPath.size)
#    draw_frame=cv2.hconcat((result,frame))
#    mask1=np.zeros((480,640),dtype=np.uint8);
    
    cv2.imshow('window',draw_frame)
    cv2.imshow('hsv',result)
    

    
    
    
    if write_on:
        out.write(draw_frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        if write_on:
            out.release()
        break
    elif k==ord('u'):
        
        UDP_active=not(UDP_active)
        print('UDP_active: ',UDP_active)
        
    

cap.release()

cv2.destroyAllWindows()