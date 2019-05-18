import Nodes

class Compressor():

    "compressor component"

    def __init__(self,inletNode,outletNode,idealoutletNode,):
        "init compressor with node"
        self.inletNode = inletNode
        self.idealoutletNode  = idealoutletNode
        self.outletNode = outletNode


    def simulate(self,node):
        "ideal"
        "assume isentropic process"
        node[self.idealoutletNode].si = node[self.inletNode].s
        node[self.idealoutletNode].ps()

        "Exp"
        "State 2 P2,T2 measured"
        node[self.outletNode].pt()
        
        "evaluate compressor work and isentropic efficiency"
        self.idealwc = node[self.idealoutletNode].h - node[self.inletNode].h
        self.wc = node[self.outletNode].h - node[self.inletNode].h
        self.eta = self.idealwc/self.wc
