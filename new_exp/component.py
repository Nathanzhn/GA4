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

    def energy_simulate(self,state):
        
        state[self.inletstate].cal()
 
        state[self.outletstate].cal()

        #evaluate compressor work and isentropic efficiency

        s_2s = state[self.inletstate].s 
        h_2s = CP.PropsSI('H','P',state[self.outletstate].p,'S',s_2s,fluid)
        ideal_w_c = h_2s-state[self.inletstate].h 
        
        self.w_c = (state[self.outletstate].h - state[self.inletstate].h)
        self.eta = ideal_w_c/self.w_c
        
    def exergy_simulate(self,state,mdot_r):
        self.w_comp =  mdot_r*self.w_c
        self.DE = mdot_r*(state[self.outletstate].h - state[self.inletstate].h\
                          -T0*(state[self.outletstate].s-state[self.inletstate].s))
        self.loss = mdot_r*T0*(state[self.outletstate].s-state[self.inletstate].s)


class Condensor():
    
    #condensor component
    def __init__(self,inletstate,outletstate):
        #init condensor state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def energy_simulate(self,state,fluid_con,mdot_con,T_con_in,T_con_out):

        p4 = CP.PropsSI('P','T',T4,'Q',0.0,fluid)
        self.dp = p4 - p1
        state[self.outletstate].p = state[self.inletstate].p -self.dp
        state[self.outletstate].cal()   

        self.cp = CP.PropsSI('C','T',T_con_in,'P',200000,fluid_con)
        self.mdot_con = mdot_con
        self.qh = state[self.inletstate].h - state[self.outletstate].h
        self.mdot_r = mdot_con*self.cp*(T_con_out-T_con_in)/(self.qh)
        
    def exergy_simulate(self,state,fluid_con,mdot_con,T_con_in,T_con_out):
        
        ds = CP.PropsSI('S','T',T_con_out,'P',200000,fluid_con)-CP.PropsSI('S','T',T_con_in,'P',200000,fluid_con)
     
        self.DE = self.mdot_r*((state[self.outletstate].h - state[self.inletstate].h)-T0*(state[self.outletstate].s-state[self.inletstate].s))
        self.con_de = mdot_con*(self.cp*(T_con_out-T_con_in)-T0*(ds))
        self.loss = -self.DE-self.con_de
        
            

class Throttle():

    #throttle component
    def __init__(self,inletstate,outletstate):
        #init throttle state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def energy_simulate(self,state):
            
        state[self.outletstate].h = state[self.inletstate].h
        state[self.outletstate].cal()
        
    def exergy_simulate(self,state,mdot_r):
        
        self.DE = mdot_r*((state[self.outletstate].h-state[self.inletstate].h)\
                            -T0*(state[self.outletstate].s-state[self.inletstate].s))
        self.loss = mdot_r*T0*(state[self.outletstate].s- state[self.inletstate].s)        

class Evaporator():
    #evaporator component
    def __init__(self,inletstate,outletstate):
        #init evaporator state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def energy_simulate(self,state,fluid_eva,mdot_r,T_eva_in,T_eva_out):        

        state[self.inletstate].xx = True

        #pressure loss and heat exchange parameters
        self.dp = state[self.inletstate].p - state[self.outletstate].p
        self.qc = state[self.outletstate].h - state[self.inletstate].h
        self.cp = CP.PropsSI('C','T',T_eva_in,'P',101500,fluid_eva)
        self.mdot_eva = (mdot_r*self.qc)/(self.cp*(T_eva_in-T_eva_out))
        
    def exergy_simulate(self,state,fluid_eva,mdot_r,T_eva_in,T_eva_out):

        self.DE = mdot_r*((state[self.outletstate].h-state[self.inletstate].h)\
                        -T0*(state[self.outletstate].s-state[self.inletstate].s))
        self.eva_de = self.mdot_eva*(self.cp*(T_eva_out-T_eva_in)-T0*(self.cp*np.log(T_eva_out/T_eva_in)))
        self.loss = -self.DE-self.eva_de