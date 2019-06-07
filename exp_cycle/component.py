import states
from conditions import *
import CoolProp.CoolProp as CP

class Compressor(): 
    
    #compressor component 
    def __init__(self,inletstate,idealoutletstate,*outletstate):
        "init compressor with state"
        self.inletstate = inletstate
        self.idealoutletstate  = idealoutletstate
        self.outletstate = outletstate

    def simulate(self,state):
        
        state[self.inletstate].cal()
 
        #ideal
        "assume isentropic process"
        state[self.idealoutletstate].p = p2
        state[self.idealoutletstate].s = state[self.inletstate].s
        #for example paper calculation
        #T3 = CP.PropsSI('T','P',p2,'Q',0.0,fluid)
        #state[self.idealoutletstate].t = T3 + 20.0
        
        state[self.idealoutletstate].cal()
        self.ideal_w_c = state[self.idealoutletstate].h - state[self.inletstate].h
        
        #Exp
        if self.outletstate:
            self.outletstate = self.outletstate[0]
            #Exp
            "State 2 P2,T2 measured"
            state[self.outletstate].cal()
    
            #evaluate compressor work and isentropic efficiency
            self.w_c = state[self.outletstate].h - state[self.inletstate].h
            self.eta = self.ideal_w_c/self.w_c


class Condensor():
    
    #condensor component
    def __init__(self,inletstate,idealoutletstate,*outletstate):
        #init condensor state
        self.inletstate = inletstate
        self.idealoutletstate  = idealoutletstate
        self.outletstate = outletstate

    def simulate(self,state,mdot_w,shc,Tw_in,Tw_out):
        #ideal
        state[self.idealoutletstate].p = state[self.inletstate].p
        state[self.idealoutletstate].x = 0.0
        state[self.idealoutletstate].cal()    
        self.ideal_qh = state[self.inletstate].h - state[self.idealoutletstate].h
        

        #Exp
        if self.outletstate:
            self.outletstate = self.outletstate[0]
            p4 = CP.PropsSI('P','T',T4,'Q',0.0,fluid)
            dp = p4 - p1
            state[self.outletstate].p = state[self.inletstate].p -dp
            state[self.outletstate].cal()        
    
            #pressure loss and heat exchange parameters
            self.dp = state[self.idealoutletstate].p - state[self.outletstate].p
            self.qh = state[self.inletstate].h - state[self.outletstate].h
            self.epsilon = mdot_w*shc*(Tw_out-Tw_in)/(self.qh*mdot_r)
            self.de = mdot_r*T0*(state[self.outletstate].s-state[self.inletstate].s)-self.qh/state[self.outletstate].t
            

class Throttle():

    #throttle component
    def __init__(self,inletstate,idealoutletstate,*outletstate):
        #init throttle state
        self.inletstate = inletstate
        self.idealoutletstate  = idealoutletstate
        self.outletstate = outletstate

    def simulate(self,state):
        #ideal
        state[self.idealoutletstate].p = p1
        state[self.idealoutletstate].h = state[self.inletstate].h
        state[self.idealoutletstate].cal()   
    
        #Exp
        if self.outletstate:
            self.outletstate = self.outletstate[0]
            
            state[self.outletstate].h = state[self.inletstate].h
            state[self.outletstate].cal()
        
        "assume change in h is negligible in throttle, so almost isenthalpic"
        "hence, no parameters to evaluate"


class Evaporator():
    #evaporator component
    def __init__(self,idealinletstate,outletstate,*inletstate):
        #init evaporator state
        self.idealinletstate  = idealinletstate
        self.inletstate = inletstate
        self.outletstate = outletstate

    def simulate(self,state,mdot_a,cp,Ta_in,Ta_out):        
        #ideal
        self.ideal_qc = state[self.idealinletstate].h - state[self.outletstate].h

        #Exp
        if self.inletstate:
            self.inletstate = self.inletstate[0]
            state[self.inletstate].xx = True

            #pressure loss and heat exchange parameters
            self.dp = state[self.inletstate].p - state[self.outletstate].p
            self.qc = state[self.inletstate].h - state[self.outletstate].h
            self.epsilon = mdot_a*cp*(Ta_in-Ta_out)/(self.qc*mdot_r)
            self.de = mdot_r*T0*(state[self.inletstate].s-state[self.outletstate].s)-self.qc/state[self.inletstate].t