import Nodes

class Evaporator():

    "evaporator component"

    def __init__(self,inletNode,outletNode,idealoutletNode):
        "init evaporator node"
        self.inletNode = inletNode
        self.idealoutletNode  = idealoutletNode
        self.outletNode = outletNode

    def simulate(self,node):
        "ideal"
        node[self.idealoutletNode].h = node[self.inletNode].h
        node[self.idealoutletNode].ph()

        "Exp"
        "State 1, P1,T1 known"
        node[self.outletNode].pt()

        "pressure loss and heat exchange parameters" # TODO
        self.dp = node[self.idealoutletNode].p - node[self.outletNode].p
        self.qc = node[self.outletNode].h - node[self.inletNode].h

    