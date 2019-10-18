# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:57:55 2019

@author: student
"""
from point import point
class line:
    def __init__(self,p1_=point(), p2_=point()):
        self.p1=p1_;
        self.p2=p2_;
        self.r=self.p2-self.p1;
    def comp_relat(self,p):
        return(p-self.p1);
    def chek_within(self,p):
        return(self.r.Vmult(comp_relat(p))>0);            
