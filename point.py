from math import sqrt,sin,cos, asin
class point:
    def __init__(self,a=0,b=0,i_=0):
        self.i=i_;
        self.x=a;
        self.y=b;
    def rotate(self):
        [self.x,self.y]=[self.y,-self.x]
        return self
    def invert(self):
        self.x=-self.x
        self.y=-self.y
        return self
    def length2(self):
        return (self.x*self.x+self.y*self.y)
    def length(self):
        self.l=sqrt(self.x*self.x+self.y*self.y)
        return(self.l)
    def __add__(self,p):
        po=point(self.x,self.y,self.i)
        po.x=po.x+p.x
        po.y=po.y+p.y
        return(po)
    def __mul__(self,a):
        b=point(self.x,self.y,self.i)
        b.x*=a;
        b.y*=a;
        return(b)
    def Vmult(self,a):
        return self.x*a.y-self.y*a.x
    def getAngle(self,p):
        Vmult_=self.Vmult(p)
        mult_=self.mult(p)
        l1=self.length()
        l2=p.length()
        mll=l1*l2
        err=0
        if(mll!=0):
            sin_=Vmult_/(l1*l2)        
        else:
            return [1,1]
        angle=asin(sin_)
#        return angle
        if(mult_>0):            
            return angle,0
        elif(Vmult_>0):
            return [3.14-angle,err]
        else:
            return [-3.14-angle,err]
        
#    def __mul__(self,v):
#        return self.x*v.x+self.y+v.y;
    def mult(self,a):
        return a.x*self.x+a.y*self.y
    def __sub__(self,p):
        po=point(self.x,self.y,self.i)
        po.x-=p.x
        po.y-=p.y
        return(po)
    def norm(self):
        err=0
        if([self.x,self.y]!=[0,0]):
            err=0
            self.length()
            self.n=self
            self.x/=(self.l+0.00001)
            self.y/=(self.l+0.00001)
            self.l=1;
        else:
            err=1
        return self,err
    def vec(self):
        return ((int(self.x),int(self.y)))
    def vecF(self):
        return (((self.x),(self.y)))