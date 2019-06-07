import Nodes
from exp import *

class Evaporator():

    "evaporator component"

    def __init__(self,inletNode,outletNode,idealinletNode):
        "init evaporator node"
        self.inletNode = inletNode
        self.idealinletNode  = idealinletNode
        self.outletNode = outletNode

    def simulate(self,node,mdot_a,cp,Ta_in,Ta_out):
        node[self.inletNode].th()
        
        "ideal"
        "the cycle based on compressor inlet"
        "node outelt = state 1"

        "Exp"
        "State 1, P1,T1 known"


        "pressure loss and heat exchange parameters" # TODO
        self.dp = node[self.inletNode].p - node[self.idealinletNode].p
        self.qc = node[self.outletNode].h - node[self.inletNode].h
        self.Qca = mdot_a*cp*(Ta_in-Ta_out)
        self.mdot_r = self.Qca/(self.qc)
    