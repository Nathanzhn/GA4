import CoolProp.CoolProp as CP

class Node(object):

    "define internal properties at node"
    def __init__(self):
        self.fluid = 'R134a'
        self.p = None
        self.t = None
        self.h = None
        self.s = None
        self.x = None
    """ self.hf = None # TODO better way to generalise
        self.hg = None # ... same as above """

    "given two properties at node, calculate the rest"
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
        "use T to find hg,hf, then use h to find x, hence actually tx"
        hg = CP.PropsSI('H','T',self.t,'Q',1.0,self.fluid)
        hf = CP.PropsSI('H','T',self.t,'Q',0.0,self.fluid)
        self.x = (self.h - hf)/(hg - hf)
        self.s = CP.PropsSI('S','T',self.t,'Q',self.x,self.fluid)
        self.p = CP.PropsSI('P','T',self.t,'Q',self.x,self.fluid)





    