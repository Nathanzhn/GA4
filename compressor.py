import Nodes

class Compressor():

    "compressor component"

    def __init__(self,inletNode,outletNode):
        "initialise compressor with node"
        self.inletNode = inletNode
        self.outletNode = outletNode

    def simulate(self,node):
        "ideal"
        node[self.outletNode].s = node[self.inletNode].s
        node[self.outletNode].ps()

        self.wc = node[self.outletNode].h - node[self.inletNode].h
