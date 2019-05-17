import Nodes

class Condensor():
    "condensor component"

    def __init__(self,inletNode,outletNode):
        "initialise node"
        self.inletNode = inletNode
        self.outletNode = outletNode

    def simulate(self,node):
        "ideal"
        node[self.outletNode].px()

        self.qh = node[self.inletNode].h - node[self.outletNode].h

