import CoolProp.CoolProp as CP
from conditions import * 

class State(object):

    #define internal properties at state
    def __init__(self):
        self.fluid = fluid #TODO
        self.p = None
        self.t = None
        self.h = None
        self.s = None
        self.x = None
        self.xx = False # True for inside vapour dome, self use only

    #given two properties at state, calculate the internal properties
    def pt(self):
        self.h = CP.PropsSI('H','P',self.p,'T',self.t,self.fluid)
        self.s = CP.PropsSI('S','P',self.p,'T',self.t,self.fluid)
        self.x = CP.PropsSI('Q','P',self.p,'T',self.t,self.fluid)
    
    def ps(self):
        self.h = CP.PropsSI('H','P',self.p,'S',self.s,self.fluid)
        self.x = CP.PropsSI('Q','P',self.p,'S',self.s,self.fluid)
        self.t = CP.PropsSI('T','P',self.p,'S',self.s,self.fluid)
    
    def ph(self):
        self.t = CP.PropsSI('T','P',self.p,'H',self.h,self.fluid)
        self.s = CP.PropsSI('S','P',self.p,'H',self.h,self.fluid)
        self.x = CP.PropsSI('Q','P',self.p,'H',self.h,self.fluid)
    def px(self):
        self.h = CP.PropsSI('H','P',self.p,'Q',self.x,self.fluid)
        self.s = CP.PropsSI('S','P',self.p,'Q',self.x,self.fluid)
        self.t = CP.PropsSI('T','P',self.p,'Q',self.x,self.fluid)

    def tx(self):
        self.h = CP.PropsSI('H','T',self.t,'Q',self.x,self.fluid)
        self.s = CP.PropsSI('S','T',self.t,'Q',self.x,self.fluid)
        self.p = CP.PropsSI('P','T',self.t,'Q',self.x,self.fluid)

    def th(self):
        #use T to find hg,hf, then use h to find x, hence actually tx()
        #this is for throttle, only works in vapour dome
        hg = CP.PropsSI('H','T',self.t,'Q',1.0,self.fluid)
        hf = CP.PropsSI('H','T',self.t,'Q',0.0,self.fluid)
        self.x = (self.h - hf)/(hg - hf)
        self.s = CP.PropsSI('S','T',self.t,'Q',self.x,self.fluid)
        self.p = CP.PropsSI('P','T',self.t,'Q',self.x,self.fluid)
        
    # calculate the state properties using any two feasible properties
    def cal(self):
        
        if self.p != None and self.h != None:
            self.ph()
        elif self.p != None and self.s != None:
            self.ps()
        elif self.p != None and self.x != None:
            self.px()   
        elif self.p != None and self.t != None and self.xx == False:
            self.pt()
        elif self.t != None and self.x != None:
            self.tx()
        elif self.t != None and self.h != None:
            self.th()
        else:
            print("Not enough properties to define state")

    