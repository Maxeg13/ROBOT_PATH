# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:29:39 2019

@author: student
"""
from point import point
import numpy as np
import cv2
from line import line
class obstacle:
    def __init__(self):
        self.mask=np.zeros((480,640),dtype=np.uint8);
        
        self.blue_mask=np.zeros((480,640,3),dtype=np.uint8);
        self.blue_mask[:,:,0]=255;
        

#        for i in range(1,ps_.size)
    def draw(self,img):
        for i in range(0,self.size):
            cv2.line(img, self.ps[i-1].vec(), self.ps[i].vec(), (255,0,0),2)
        return img
    def createMask(self,ps_):
        self.ps=ps_;
        self.size=len(ps_);
        self.lines=[];        
        for i in range(0,self.size):
            self.lines.append(line(self.ps[i],self.ps[i-1]));
            
        for i in range(0,480):
            for j in range(0,640):
                p=point(j,i)
                h_=True;
                for ln in self.lines:
                    if(ln.check_outside(p,35)): 
                        self.mask[i][j]=1;
                        
                    if(ln.check_within_p1(p,35)):
                        self.mask[i][j]=1;
                        
                    if(not ln.check_within(p)):
                        h_=False;
                if(h_):
                    self.mask[i][j]=1;
                    
    def createAuxMasks(self):                    
        self.not_mask=np.uint8(cv2.bitwise_not(self.mask*255)/255);
        self.blue_mask=cv2.bitwise_and(self.blue_mask,self.blue_mask,mask = self.mask);
                
                        
                        
        
    
