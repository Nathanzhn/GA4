import states
from conditions import *
import CoolProp.CoolProp as CP
import numpy as np

class Compressor(): 
    
    #compressor component 
    def __init__(self,inletstate,outletstate):
        "init compressor with state"
        self.inletstate = inletstate
        self.outletstate = outletstate

    def simulate(self,state,eta):
        
        state[self.inletstate].cal()
 
        self.eta = 0.65
        state[self.outletstate].p = p2
        s_2s = state[self.inletstate].s
        h_2s = CP.PropsSI('H','P',state[self.outletstate].p,'S',s_2s,fluid)
        state[self.outletstate].h = state[self.inletstate].h \
        +(h_2s - state[self.inletstate].h)/self.eta
        state[self.outletstate].cal()
        
        self.w_c = state[self.outletstate].h - state[self.inletstate].h
        self.loss = -mdot_r*T0*(state[self.outletstate].s-state[self.inletstate].s)
                            

class Condensor():
    
    #condensor component
    def __init__(self,inletstate,outletstate):
        #init condensor state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def simulate(self,state,mdot_w,Tw_in,Tw_out):
        #ideal
        state[self.outletstate].x = 0.0
        dp = 200000
        state[self.outletstate].p = state[self.inletstate].p -dp
        state[self.outletstate].cal()     
        self.cp_w = CP.PropsSI('C','T',Tw_in,'P',100000,'water')

        self.qh = state[self.inletstate].h - state[self.outletstate].h
        self.epsilon = mdot_w*self.cp_w*(Tw_out-Tw_in)/(self.qh*mdot_r)
        
        ds = CP.PropsSI('S','T',Tw_out,'P',100000,'water')-CP.PropsSI('S','T',Tw_in,'P',100000,'water')
        
        self.loss = -mdot_r*((state[self.outletstate].h-state[self.inletstate].h)\
                            -T0*(state[self.outletstate].s-state[self.inletstate].s))\
                            -mdot_w*(self.cp_w*(Tw_out-Tw_in)-T0*(ds))

class Throttle():

    #throttle component
    def __init__(self,inletstate,outletstate):
        #init throttle state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def simulate(self,state):
        
        state[self.outletstate].h = state[self.inletstate].h
        state[self.outletstate].cal()

        self.loss = -mdot_r*T0*(state[self.outletstate].s- state[self.inletstate].s)        

class Evaporator():
    #evaporator component
    def __init__(self,inletstate,outletstate):
        #init evaporator state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def simulate(self,state,mdot_a,Ta_in,Ta_out):        

        self.dp = state[self.inletstate].p - state[self.outletstate].p
        self.qc = state[self.inletstate].h - state[self.outletstate].h
        cp_a = (CP.PropsSI('C','T',Ta_in,'P',100000,'air')+CP.PropsSI('C','T',Ta_out,'P',100000,'air'))/2
        self.epsilon = mdot_a*cp_a*(Ta_in-Ta_out)/(self.qc*mdot_r)
        
        self.loss = -mdot_r*((state[self.outletstate].h-state[self.inletstate].h)\
                             -T0*(state[self.inletstate].s-state[self.outletstate].s))\
                             -mdot_w*(cp_a*(Ta_out-Ta_in)-T0*(cp_a*np.log(Ta_out/Ta_in)))