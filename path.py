import cv2
import numpy as np
from point import point

class path:
    def __init__(self,a,b):
        self.targ_mask=np.zeros((480,640),dtype=np.uint8);
        self.targ_red_mask=np.zeros((480,640,3),dtype=np.uint8);
        self.targ_red_mask[:,:,2]=255;
        
        self.stop=0
        self.i=0
        self.pt=point()
        self.size=a.size# hooooooooow?????
        self.ps=[]# ps - points
        self.tau=[]
        self.n=[]
        for i in range(0,self.size):
            p1=point(a[i],b[i],i)
            self.ps.append(p1)
    def draw(self,img):
        for i in range(1,self.size):
            cv2.line(img,self.ps[i-1].vec(),self.ps[i].vec(),(255,0,0),2)
        return img
    def comp_n(self): 
        self.tau=[]
        self.n=[]
        for i in range(1,self.size):
            self.tau.append(self.ps[i]-(self.ps[i-1]))
        for i in range(0,self.size-1):
#            self.tau[i]=self.ps[i].minus(self.ps[i-1])
            self.tau[i].norm()
            
        for i in range(1,self.size-1):
            n_=self.tau[i]-(self.tau[i-1])
#            tau_.norm()
            if(n_==0):
                n_=self.tau[i]
                n_.rotate()
                
            if(n_.Vmult(self.ps[i]-self.ps[i-1])<0):
                n_.invert();
            self.n.append(n_);
    def is_right(self, p1, i):
        
        p1=p1-(self.ps[i+1])
        p2=self.n[i]
        res=p1.Vmult(p2)
        if(res>0):
            return True
        else:
            return False
    def check_reached(self,p):
        if(not(self.is_right(p,self.i))):
            
            self.i+=1;
        if(self.i==(self.size-2)):
            self.stop=1
            self.i-=1;
            
        self.pt=self.ps[self.i+1]
        
    def create_targ_mask(self,ind):
        p_=self.ps[self.size-1]
        for i in range(0,480):
            for j in range(0,640):                
                if((p_-point(j,i)).length2()<(ind*ind)):
                    self.targ_mask[i,j]=1;
        self.targ_red_mask=cv2.bitwise_and(self.targ_red_mask,self.targ_red_mask,mask = self.targ_mask);

        