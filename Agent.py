import numpy as np
from point import point
from globals import *

class Agent:    
    def __init__(self):
        self.mask=np.zeros((screen_size[0],screen_size[1]),dtype=np.uint8)
        self.mask[20,20]=1;
        self.rad=23
        self.dirs_ptr=0;
        self.dirs_cnt=0;
        self.dphi=0;        
        self.dirs=[point()]*10;
        self.dirh=point(1,0);
        self.dir=point(1,0);
        self.pp=point(1,0);
        self.p=point(1,0);
        self.p1=point();
        self.phi=0;
    def comp_dphi(self,p):
        dphi_,err=self.v.getAngle(p-self.p)
        if(err!=1):
            self.dphi=dphi_
            
    def setP(self,p):
        self.pp=self.p
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
            
    def comp_dir2(self,dir1):   
            self.dirs[self.dirs_ptr]=dir1
            self.dirs_ptr+=1
            if(self.dirs_ptr==len(self.dirs)):
                self.dirs_ptr=0
            
            bb=point()
            for ab in self.dirs:
                bb=bb+ab
#            print(self.bb.vec())
            dir,err =bb.norm()
            
            if(err==0):
                self.dir=dir
            
        
    def go_(self,targ):# _ is for what??
#        print(self.p.vecF())
        
        self.p+=(self.v*4);
        
        self.comp_dphi(targ)
        if((self.p-targ).length2()>100):
            self.phi+=self.dphi*0.07;        
        self.v=point(cos(self.phi),sin(self.phi));