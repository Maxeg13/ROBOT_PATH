import cv2
from point import point

class path:
    def __init__(self,a,b):
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
#        print(self.pt.vec())
#        print(not(self.is_right(p,self.i)))
        if(not(self.is_right(p,self.i))):
            
            self.i+=1;
        if(self.i==(self.size-2)):
            self.stop=1
            self.i-=1;
            
        self.pt=self.ps[self.i+1]