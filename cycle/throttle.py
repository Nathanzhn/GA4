import Nodes
from exp import *

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


