#C:\Users\student\Documents\MATLAB\avacir\avacir\avacir.m
import cv2
import numpy as np
from Agent import Agent
from random import random 
#from pyimagesearch import imutils
from point import point
from path import path
from obstacle import obstacle
import socket
from msvcrt import getch
from math import sqrt,sin,cos, asin
import warnings
from globals import *

warnings.filterwarnings('ignore')

cir_size=128
del_cnt=35;
path_draw=True;
write_video_on=0;
Debug=0;
file_save=0;
file_load=0;
file_obstacle_2_load='obstacle1.txt';
file_obstacle_2_save='avcir_obst.csv';
#load_obstacle=False;

UDP_algor_active=0
UDP_algor_active_h=UDP_algor_active
rot_speed_k=26
speed_init=120
speed=speed_init#60
IP='169.254.104.146'
PORT=49122
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
UDP_cnt=0


#UDP_active=True
#
x_=np.array([170,200,250,300,350,400,450])
x_+=100
y_=np.array([100,88,80,120,140,180,200])


x_=np.array([560,550,500,400,300,200,100])
y_=np.array([200,180,140,120,80,110,100])

y_+=140

time=0

def getMask(src_frame,hsv,hsv_list):
    wind=20;
    lower_blue1 = np.array([hsv_list[0],hsv_list[1],hsv_list[2]])
    lower_blue2 = np.array([0,hsv_list[1],hsv_list[2]])
    
    upper_blue1 = np.array([min(180,hsv_list[0]+wind),255,255])
    upper_blue2 = np.array([max(-1,hsv_list[0]+wind-180),255,255])
    mask = cv2.inRange(hsv,lower_blue1, upper_blue1)
    mask_h= cv2.inRange(hsv,lower_blue2, upper_blue2)
    mask|=mask_h
#    mask=mask_h
#    mask=~mask
#masked_img=src_frame.copy()
    masked_img = cv2.bitwise_and(src_frame,src_frame,mask = mask)#whaaaaaaaaaaaaaaaaaaat?????????
    return masked_img;

def saveFile(name, data):
#    data2=data.copy()
    data2=cv2.resize(data,(cir_size,cir_size))
    file = open('C:/Users/student/Documents/MATLAB/avacir/avacir/'+name,"w"); 
    for i in range(0,cir_size):
        for j in range(0,(cir_size-1)):
            file.write(str(np.int(data2[i][j]))+';'); 
        file.write(str(np.int(data2[i][127]))); 
        file.write('\n');
    file.close();
        
def loadFile(name):     
    data=np.zeros((screen_size[0],screen_size[1]),dtype=np.uint8)    
    file = open(name, "r");
    for i in range(0,screen_size[0]):
        l=file.readline()[0:screen_size[1]:2];
        for j in range(0,screen_size[1]):
            data[i,j]=int(l[j]);  
    file.close();
    return data
        
    



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
    
#    return 1...>..
#    return sums
mY=1
mX=1 
    
    
    
    


pioneer=Agent();

#__________what the ...
#saveFile("pioneer.txt",pioneer.mask)
#y_=np.array([100,200,100,100,100,100,100])
      




pioneerPath=path(x_,y_) #bad __ 
pioneerPath.comp_n()
targ=point(x_[-1],y_[-1])   


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
    
    
    
if(Debug):
    cap = cv2.VideoCapture(1)
else:
    cap = cv2.VideoCapture(1)
    
cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(screen_size[1]))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(screen_size[0]))

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('hsv')
cv2.namedWindow('window')

# Starting with 100 to prevent error while masking
h,s,v = 86,120,119

# Creating track bar
cv2.createTrackbar('h', 'window',0,179,nothing)
h = cv2.setTrackbarPos('h','window', h)

cv2.createTrackbar('s', 'window',0,255,nothing)
s = cv2.setTrackbarPos('s','window', s)

cv2.createTrackbar('v', 'window',0,255,nothing)
v=cv2.setTrackbarPos('v','window', v)




#size = 480, 640, 3
accumed_img=np.zeros(screen_size, dtype=np.uint8)





if write_video_on:
#    self._fourcc = VideoWriter_fourcc(*'MP4V')
#self._out = VideoWriter(self._name, self._fourcc, 20.0, (640,480))
    out=cv2.VideoWriter('hsv_.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 24, (screen_size[1],screen_size[0]))
#    out = cv2.VideoWriter('hsv_.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 24, (640,480))





def click_and_crop(event, x, y, flags,ss):
    if(event==cv2.EVENT_LBUTTONDOWN):
        p=point(x,y)
        global targ,obs_ps,obs,draw_obs,pioneer,kernel_circ,targ_mask
        targ=p
#        print(pioneer.rad)
        targ_mask=np.zeros([screen_size[0], screen_size[1]], dtype=np.uint8)
        targ_mask[(targ.y-pioneer.rad):(targ.y+pioneer.rad+1), (targ.x-pioneer.rad):(targ.x+pioneer.rad+1)]=kernel_circ
#        obs_ps.append(p)
        
#        if(len(obs_ps)==4):
#            
#            obs.createMask(obs_ps,25);
#            obs.createAuxMasks();
#            
#            draw_obs=1;
#            if(file_save):
#                saveFile(file_obstacle_2_save,  obs.mask);
cv2.setMouseCallback("window", click_and_crop)

        

#print(pioneerPath.p);

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def drive(rot,speed):
    if(kbd_rot<0):
        sock.sendto(bytes([np.uint8(255), np.uint8(rot),np.uint8(1),np.uint8(speed)]), (IP, PORT))
    else:
        sock.sendto(bytes([0, np.uint8(kbd_rot), np.uint8(1), np.uint8(speed)]), (IP, PORT))


#sock.sendto(bytes([np.uint8(255), np.uint8(rot),np.uint8(1),np.uint8(speed)]), (IP, PORT))
 
    
    
    
obs_ps=[];
cX=2;
cY=2;


obs=obstacle();


if(file_load):
    obs.mask=loadFile(file_obstacle_2_load).copy()
    
    
if(file_load):   
    obs.createAuxMasks();      
    draw_obs=1;
else:
    draw_obs=0;    

pioneerPath.create_targ_mask(pioneer.rad);
#saveFile('targ.txt',pioneerPath.targ_mask)
size = 40, 40, 3
#import
hsv_rect=np.zeros(size, dtype=np.uint8)
write_frame=np.zeros([screen_size[0], screen_size[1],3], dtype=np.uint8)
trace_mask=np.zeros([screen_size[0], screen_size[1]], dtype=np.uint8)
targ_mask=np.zeros([screen_size[0], screen_size[1]], dtype=np.uint8)

kernel_size=pioneer.rad*2+1
kernel_circ=np.zeros((kernel_size,kernel_size),np.float);
_centre=point(int(kernel_size/2),int(kernel_size/2))
for i in range(0,kernel_size):
    for j in range(0, kernel_size):
        p=point(j,i)
        if((p-_centre).length()<kernel_size/2):
            kernel_circ[i,j]=1;
kernel_circ=kernel_circ*2550/kernel_circ.sum();            
#kernel_circ[::5,::5,0]

# Obviously keyboard's prefix
kbd_speed=0;
kbd_rot=0;
help_pt=point(1,0);


while(1):
    
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

    hsv_rect[:,:,0]=h
    hsv_rect[:,:,1]=s
    hsv_rect[:,:,2]=v
    hsv_rect=cv2.cvtColor(hsv_rect,cv2.COLOR_HSV2BGR)

        
#    wind=v;
#    k=0.15;
#    upper_blue = np.array([180,255,255])
#    upper_blue = np.array([thresh(h+wind,180),thresh(s+wind,255),thresh(v.+wind,255)])


    kernel = np.ones((7,7),np.float32)/49
    hsv = cv2.filter2D(hsv,-1,kernel)
    
    
#    88 183 224 (search blue)
#    
    if(Debug):
        masked_img_obsts=getMask(src_frame,hsv,[h, s, v]);
    else:
        masked_img_obsts=getMask(src_frame,hsv,[16, 101, 215]);
        
        
#    masked_img_pioneer=getMask(src_frame,hsv,[81, 54, 226]);
        masked_img_pioneer=getMask(src_frame,hsv,[h, s, v]);
#    result=cv2.blur(result,(10,10))
#    k=0.9
#    accumed_img=cv2.addWeighted(masked_img,k,accumed_img,1-k,0)
   # calculate moments of binary image
#     ..
    result_pioneer=masked_img_pioneer.copy()
    result_obsts=masked_img_obsts.copy()#for drawing vectors
    
#    alpha=0.5;   
#    beta = ( 1.0 - alpha );
#    cv2.addWeighted( result, alpha, hsv_rect, beta, 0.0, result);
#    result=result|hsv_rect
#     [cY,c]

    gray = cv2.cvtColor(result_pioneer, cv2.COLOR_BGR2GRAY)
    M=cv2.moments(gray)
    if(M["m00"]!=0):
        cX = int(M["m10"] / M["m00"]) 
        cY = int(M["m01"] / M["m00"])
        
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
    

#    else:
#        cX=640;
#        cY=480;
    if(time==2):
        trace_mask=np.zeros([screen_size[0], screen_size[1]], dtype=np.uint8)
    if(time>3):
        
        pioneerPath.check_reached(pioneer.p);

    
#    mask
#    [mY1,Err1]=pre_median_y(mask)
#    if(not(Err1)):
#        mY=mY1
#    mX=320

    pioneer.setP(point(cX, cY))
    cv2.line(trace_mask,(pioneer.p).vec(),(pioneer.pp).vec(),(255,255,255))

    
    
#    dangerous_________________________________________
#    pioneer.comp_dir();
    
    dphi_,err=(pioneerPath.pt-pioneer.p).getAngle(pioneer.dir)#bad coding is here
    err2=0
    if((pioneerPath.pt-pioneer.p).length2()<200):  
        err2=1
        pioneer.dphi=dphi_*rot_speed_k*0.5
#        print((pioneerPath.pt-pioneer.p).length2())
        
    if((err==0) and (err2==0)):
        pioneer.dphi=dphi_*rot_speed_k
    
#    if(time==38):
#        pioneerPath=path(x_,y_) #bad __ 
#        pioneerPath.comp_n()        
    
    
    
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
        if(UDP_algor_active): 
            print(speed)
            if(rot_speed<0):
                sock.sendto(bytes([np.uint8(255), np.uint8(rot_speed),0,speed]), (IP, PORT))
            else:
                sock.sendto(bytes([0, np.uint8(rot_speed), 0,speed]), (IP, PORT))
    if UDP_algor_active_h and not(UDP_algor_active):#            
        sock.sendto(bytes([0,0,0,0]), (IP, PORT))
            
    UDP_algor_active_h=UDP_algor_active
    
#    pioneer.go(pioneerPath.pt);
    
    
#draw_frame=src_frame
#    for r in range(0,30):
#        alpha=random()*6.28;
#        l=8
#        if((result_pioneer[pioneer.p.y+np.int(l*np.sin(alpha)),pioneer.p.x+np.int(l*np.cos(alpha))]!=[0,0,0]).any()):
#            cv2.line(draw_frame,(pioneer.p).vec(),(pioneer.p+point(np.int(l*np.cos(alpha)),np.int(l*np.sin(alpha)))).vec(),(255, 0, 255));



    draw_frame=src_frame


#______________orientation
    l=8
#    l=20
    ptsum=point(0,0);
    for r in range(0,45):
        alpha=random()*6.28;
#        l=7# old
        
        dir_=point(l*np.cos(alpha),l*np.sin(alpha))
        if(l<pioneer.p.y<(screen_size[0]-l)and(l<pioneer.p.x<(screen_size[1]-l))):
            if((result_pioneer[pioneer.p.y+np.int(dir_.y),pioneer.p.x+np.int(dir_.x)]!=[0,0,0]).any()):
                if(pioneer.dirh.mult(dir_)<0):
                    dir_.invert();
                ptsum=ptsum+dir_;
    ptsum.norm();
    if((ptsum.x==0)and(ptsum.y==0)):    
        1
    else:
        pioneer.dirh=ptsum;
        pioneer.comp_dir2(pioneer.dirh)
    cv2.line(draw_frame,(pioneer.p).vec(),(pioneer.p+pioneer.dir*l).vec(),(255, 0, 255));
    cv2.line(result_pioneer,(pioneer.p).vec(),(pioneer.p+pioneer.dir*l).vec(),(255, 0, 255));
            
#                else:
#                    print('NO')
#    cv2.circle(draw_frame, (cX, cY), 1, (255, 255, 255), -1)
    phrase=['phrase one','phrase two','phrase three']
#    cv2.putText(draw_frame, phrase[min(pioneerPath.i,0)], (cX - 25, cY - 40),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0,100), 1)

#    if()
#    print(pioneerPath.is_right(DR.p,0))
#    print(targ.vec())
    if(path_draw):
        cv2.circle(draw_frame, pioneerPath.pt.vec(), 5, (0, 255, 255), -1)
    
    
    cv2.circle(result_pioneer, pioneer.p.vec(), 3, (255, 0, 255), -1)
#    cv2.circle(result_pioneer, pioneerPath.pt.vec(), 5, (0, 255, 255), -1)
    
#    cv2.circle(result, (20,20), 20, (255, 0, 255), -1)
#    pts_=np.array([(1,1),(1,20),(20,20)]);
#    cv2.fillPoly(result,pts_,(255,255,255))
    
    
#    IMPORTANT
#    result=cv2.cvtColor(result,cv2.COLOR_HSV2BGR);
    result_kerneled=cv2.filter2D(result_obsts, cv2.CV_8UC1, kernel_circ);
    result_mask = cv2.inRange(result_kerneled,0,150)
    result_mask=255-result_mask
    
    draw_frame[0:40,0:40]=hsv_rect.copy()    
    cv2.line(draw_frame,pioneer.p.vec(),(pioneer.p+(pioneer.dir*27)).vec(),(0,255,0),2)
    if(path_draw):
        draw_frame=pioneerPath.draw(draw_frame)     
    draw_frame[:,:,0]|=result_mask;
    draw_frame[:,:,2]|=targ_mask*255;
    
    draw_frame[:,:,1]|=trace_mask;
    draw_frame[:,:,0]&=255-trace_mask;
    draw_frame[:,:,2]&=255-trace_mask;
    
    cv2.circle(draw_frame, pioneer.p.vec(), 3, (255, 0, 255), -1)
    dd=draw_frame.copy()
#    draw_frame=cv2.resize(draw_frame,(128,128))
#    draw_frame[200][100]=[255,255,255]
   
    #for mouse generated obs
    if(draw_obs):
#        draw_frame = obs.draw(draw_frame)
#        draw_frame = cv2.bitwise_and(draw_frame,draw_frame,mask = obs.not_mask)
#        draw_frame=draw_frame|obs.blue_mask;
        draw_frame=draw_frame|pioneerPath.targ_red_mask;
        cv2.line(draw_frame,pioneer.p.vec(),(pioneer.p+(pioneer.dir*27)).vec(),(0,255,0),2)
        draw_frame|=result_mask;
#        draw_frame=draw_frame|pioneer.mask*255;
        #|pioneer.mask*255;
#        cv2.imshow('hsv',obs.blue_mask)
#    print(pioneerPath.size)
#    draw_frame=cv2.hconcat((result,frame))
#    mask1=np.zeros((480,640),dtype=np.uint8);
#    result_pioneer
    
    
    cv2.imshow('window',draw_frame)
    cv2.imshow('result_obsts', result_obsts)
#    cv2.imshow('mask', targ_mask*255)
#    cv2.imshow('mask', targ_mask*255)
    cv2.imshow('pioneer coords',result_pioneer)
    

    
    
#    write_frame[0:480,:,:]=draw_frame.copy()
#    write_frame[480:960,:,:]=draw_frame.copy()    
    if write_video_on:
        out.write(draw_frame)
        
        

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        if write_video_on:
            out.release()
        break
    elif k==ord('u'):        
        UDP_algor_active=not(UDP_algor_active)
        print('UDP_active: ',UDP_algor_active)
        if(UDP_algor_active):
            speed=speed_init
    elif k==ord('o'):#'s' is already busy
        saveFile(file_obstacle_2_save,result_mask/255)
        #save the robot's starting position
        file = open('C:/Users/student/Documents/MATLAB/avacir/avacir/avcir_start.csv',"w"); 
        file.write(str(np.int(pioneer.p.x/screen_size[1]*cir_size))+';'+str(np.int(pioneer.p.y/screen_size[0]*cir_size))); 
        file.write('\n');
        file.close();
        
        saveFile('avcir_target.csv',targ_mask)
        print('data saved')
       
        
        #Debug drive
    elif k==ord('a'): 
        kbd_rot+=(10);
        drive(kbd_rot,kbd_speed);
    elif k==ord('d'):
        kbd_rot-=(10);
        drive(kbd_rot,kbd_speed);
    elif k==ord('w'):         
        kbd_speed+=(10);
        print(kbd_speed)
        drive(kbd_rot,kbd_speed);       
    elif k==ord('s'):
        kbd_speed-=(10);
        print(kbd_speed);
        drive(kbd_rot,kbd_speed);
        #reverse vector
    elif k==ord('r'):
        for a in pioneer.dirs:
            a.x=-a.x;
            a.y=-a.y;
        
        
    elif k==ord('h'):
        kbd_speed=0;
        kbd_rot=0;
        sock.sendto(bytes([np.uint8(0), np.uint8(0),np.uint8(0),np.uint8(0)]), (IP, PORT))
    elif k==ord('l'):
        
        x_=[];
        y_=[];
        file = open('C:/Users/student/Documents/MATLAB/avacir/avacir/avcir_trectory.csv', "r");
        str_=file.readline();
        xx=str_.split(';')
        for j in range(0,len(xx)):
            x_.append(int(xx[j]));  
        str_=file.readline();
        file.close();
        
        xx=str_.split(';')
        for j in range(0,len(xx)):
            y_.append(int(xx[j]));               
            
#        for k in range(0,del_cnt):
#            del x_[-2]
#            del y_[-2]
        

        x_=np.array(x_)
        y_=np.array(y_)
        

        
        x_*=round(float(screen_size[1])/cir_size)
        y_*=round(float(screen_size[0])/cir_size)
        y_-=19
#        y_+=65
        
        
        
        pioneerPath=path(x_,y_) #bad __ 
        pioneerPath.comp_n()        
    elif k==ord('e'):
        trace_mask=np.zeros([screen_size[0], screen_size[1]], dtype=np.uint8)
    elif k==ord('p'):
        path_draw=not path_draw
    elif k==ord('i'):
        del_cnt+=1;
        

cap.release()

cv2.destroyAllWindows()