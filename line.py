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
    def check_within(self,p):
        return(self.r.Vmult(self.comp_relat(p))<0);      
    def check_within_length(self,p):
        a=self.comp_relat(p).mult(self.r);
        return(a>0 and a<self.r.length2());
    def check_outside(self,p,ind):
        if(self.check_within_length(p)):
            a=self.r.Vmult(self.comp_relat(p))/self.r.length();
            if(a>=0 and a<(ind)):
                return True;
        return False;
    
    def check_within_p1(self,p,ind):
        a=p-self.p1;
        l2=a.length();
        
        return(l2<ind);
