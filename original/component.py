import Nodes
from exp_data import *
import CoolProp.CoolProp as CP

class Compressor():

    "compressor component"
    


    def __init__(self,inletNode,outletNode,idealoutletNode,):
        "init compressor with node"
        self.inletNode = inletNode
        self.idealoutletNode  = idealoutletNode
        self.outletNode = outletNode


    def simulate(self,node):

        node[self.inletNode].pt()
  
        "Exp"
        "State 2 P2,T2 measured"
        node[self.outletNode].pt()

        
        "ideal"
        "assume isentropic process"
        node[self.idealoutletNode].p = p2
        node[self.idealoutletNode].s = node[self.inletNode].s
        node[self.idealoutletNode].ps()


        
        "evaluate compressor work and isentropic efficiency"
        self.idealwc = node[self.idealoutletNode].h - node[self.inletNode].h
        self.wc = node[self.outletNode].h - node[self.inletNode].h
        self.eta = self.idealwc/self.wc

class Condensor():
    "condensor component"

    def __init__(self,inletNode,outletNode,idealoutletNode):
        "init condensor node"
        self.inletNode = inletNode
        self.idealoutletNode  = idealoutletNode
        self.outletNode = outletNode


    def simulate(self,node,mdot_w,shc,Tw_in,Tw_out):
        node[self.inletNode].pt()

        """ "Exp"
        node[self.outletNode].x = 0.0
        node[self.outletNode].tx() """

        # Exp based on pressure loss in evaporator
        p4 = CP.PropsSI('P','T',T4,'Q',0.0,fluid)
        dp = p4 - p1
        print(dp)
        node[self.outletNode].p = node[self.inletNode].p -dp
        node[self.outletNode].pt()

        "ideal"
        node[self.idealoutletNode].p = node[self.inletNode].p
        node[self.idealoutletNode].x = 0.0
        node[self.idealoutletNode].px()

        "pressure loss and heat exchange parameters" # TODO
        self.dp = node[self.idealoutletNode].p - node[self.outletNode].p
        self.qh = node[self.inletNode].h - node[self.outletNode].h
        self.Qhw = mdot_w*shc*(Tw_out-Tw_in)
        self.epsilon = self.Qhw/(self.qh*mdot_r)


class Throttle():

    "throttle component"
    


    def __init__(self,inletNode,outletNode,idealoutletNode):
        "init throttle node"
        self.inletNode = inletNode
        self.idealoutletNode  = idealoutletNode
        self.outletNode = outletNode

    def simulate(self,node):
        node[self.inletNode].pt()

        "Exp"
        node[self.outletNode].h = node[self.inletNode].h
        node[self.outletNode].th()

        "ideal"
        node[self.idealoutletNode].p = p1
        node[self.idealoutletNode].h = node[self.inletNode].h
        node[self.idealoutletNode].ph()
        

        "assume change in h is negligible in throttle, so almost isenthalpic"
        "hence, no parameters to evaluate"

class Evaporator():

    "evaporator component"

    def __init__(self,inletNode,outletNode,idealinletNode):
        "init evaporator node"
        self.inletNode = inletNode
        self.idealinletNode  = idealinletNode
        self.outletNode = outletNode

    def simulate(self,node,mdot_a,cp,Ta_in,Ta_out):
        #node[self.inletNode].th()
        
        "ideal"
        "the cycle based on compressor inlet"
        "node outelt = state 1"

        "Exp"
        "State 1, P1,T1 known"


        "pressure loss and heat exchange parameters" # TODO
        self.dp = node[self.inletNode].p - node[self.idealinletNode].p
        self.qc = node[self.outletNode].h - node[self.inletNode].h
        self.Qca = mdot_a*cp*(Ta_in-Ta_out)
        self.epsilon = self.Qca/(self.qc*mdot_r)