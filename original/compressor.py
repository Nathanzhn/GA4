import Nodes
from exp import *

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
