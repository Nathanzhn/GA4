import Nodes

class Condensor():
    "condensor component"

    def __init__(self,inletNode,outletNode,idealoutletNode):
        "init condensor node"
        self.inletNode = inletNode
        self.idealoutletNode  = idealoutletNode
        self.outletNode = outletNode

    def simulate(self,node):
        "ideal"
        node[self.idealoutletNode].px()

        "Exp"
        node[self.outletNode].th()

        "pressure loss and heat exchange parameters" # TODO
        self.dp = node[self.idealoutletNode].p - node[self.outletNode].p
        self.qh = node[self.inletNode].h - node[self.outletNode].h
