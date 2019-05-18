import Nodes

class Throttle():

    "throttle component"

    def __init__(self,inletNode,outletNode,idealoutletNode):
        "init throttle node"
        self.inletNode = inletNode
        self.idealoutletNode  = idealoutletNode
        self.outletNode = outletNode

    def simulate(self,node):
        "ideal"
        node[self.idealoutletNode].h = node[self.inletNode].h
        node[self.idealoutletNode].ph()
        
        "Exp"
        node[self.outletNode].th()

        "assume change in h is negligible in throttle, so almost isenthalpic"
        "hence, no parameters to evaluate"


