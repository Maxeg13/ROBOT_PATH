# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 17:29:39 2019

@author: student
"""
import numpy as np
import cv2
from line import line
class obstacle:
    def __init__(self, ps_):
        self.mask=np.zeros((480,640),dtype=np.uint8);
        self.ps=ps_;
        self.size=len(ps_);
        self.lines=[];
        for i in range(0,self.size):
            self.lines.append(line(self.ps[i],self.ps[i-1]));
#        for i in range(1,ps_.size)
    def draw(self,img):
        for i in range(0,self.size):
            cv2.line(img, self.ps[i-1].vec(), self.ps[i].vec(), (255,0,0),2)
        return img
