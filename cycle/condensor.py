import Nodes

class Condensor():
    "condensor component"

    def __init__(self,inletNode,outletNode,idealoutletNode):
        "init condensor node"
        self.inletNode = inletNode
        self.idealoutletNode  = idealoutletNode
        self.outletNode = outletNode

    def simulate(self,node):
        node[self.inletNode].pt()

        "Exp"
        node[self.outletNode].x = 0.0
        node[self.outletNode].tx()

        "ideal"
        node[self.idealoutletNode].p = node[self.inletNode].p
        node[self.idealoutletNode].x = 0.0
        node[self.idealoutletNode].px()

        "pressure loss and heat exchange parameters" # TODO
        self.dp = node[self.idealoutletNode].p - node[self.outletNode].p

        self.qh = node[self.inletNode].h - node[self.outletNode].h
