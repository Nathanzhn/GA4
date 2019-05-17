import Nodes

class Evaporator():

    "evaporator component"

    def __init__(self,inletNode,outletNode):
        "initialise node"
        self.inletNode = inletNode
        self.outletNode = outletNode

    def simulate(self,node):
        "ideal"
        node[self.outletNode].h = node[self.inletNode].h
        node[self.outletNode].ph()

        self.qc = node[self.outletNode].h - node[self.inletNode].h

    