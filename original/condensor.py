import Nodes
from exp import *
import CoolProp.CoolProp as CP

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
        p4 = CP.PropsSI('P','T',node[self.outletNode].t,'Q',0.0,fluid)
        dp = p4 - p1
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
        self.mdot_r = self.Qhw/(self.qh)
        
