import Nodes

class Throttle():

    "throttle component"

    def __init__(self,inletNode,outletNode):
        "initialise compressor with node"
        self.inletNode = inletNode
        self.outletNode = outletNode

    def simulate(self,node):
        "ideal"
        node[self.outletNode].h = node[self.inletNode].h
        node[self.outletNode].ph()

