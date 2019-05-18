import Nodes

class Evaporator():

    "evaporator component"

    def __init__(self,inletNode,outletNode,idealinletNode):
        "init evaporator node"
        self.inletNode = inletNode
        self.idealinletNode  = idealinletNode
        self.outletNode = outletNode

    def simulate(self,node):
        node[self.inletNode].th()
        
        "ideal"
        "the cycle based on compressor inlet"
        "node outelt = state 1"

        "Exp"
        "State 1, P1,T1 known"


        "pressure loss and heat exchange parameters" # TODO
        self.dp = node[self.idealinletNode].p - node[self.outletNode].p
        self.qc = node[self.outletNode].h - node[self.inletNode].h

    