from Nodes import *
from compressor import *
from condensor import *
from throttle import *
from evaporator import *
from exp import *






"0-3 Exp nodes, 4-7 Ideal nodes"
"for ideal p1,p2 are given"
nodes = [Node() for i in range(7)]
nodes[0].p = p1
nodes[0].t = T1
nodes[1].p = p2
nodes[1].t = T2
nodes[2].t = T3
nodes[3].t = T4

""" #assumption in Exp components
nodes[2].x = 0.0 # condenser ideal state at outlet is saturated liquid 
nodes[3].h = nodes[2].h #throttle isenthalpic process """

""" # assumption in ideal components
nodes[5].s = nodes[1].s # compressor isentropic process
nodes[6].x = 0.0 # condenser ideal state at outlet is saturated liquid 
nodes[6].p = nodes[1].p # condenser p3=p2, no pressure loss
nodes[7].p = nodes[0].p # evaporator p4 = p1, no pressure loss
nodes[7].h = nodes[2].h #throttle isenthalpic process """

# 2 connect device
c = Compressor(0, 1, 4)
d = Condensor(1, 2, 5)
t = Throttle(2, 3, 6)
e = Evaporator(3,0, 6)



c.simulate(nodes)    
d.simulate(nodes) 
t.simulate(nodes)      
e.simulate(nodes)
#print(nodes[2].p)
#    myobj = attributes = [attr for attr in dir(nodes[2]) if not attr.startswith('__')]
plt_hc = [nodes[i].h/1000.0 for i in range(4)]
plt_pc = [nodes[i].p for i in range(4)]

plt_hc.append(nodes[0].h/1000.0)
plt_pc.append(nodes[0].p)





import CoolProp.CoolProp as CP
import numpy as NP
import matplotlib.pyplot as plt

#fluid = input ('Enter fluid name: ')
fluid = 'R134a'


pc = CP.PropsSI (fluid,'pcrit')
pt = CP.PropsSI (fluid,'ptriple')

# Create lists of properties on saturation line with GP variation in p

pr = (0.9999 * pc / pt)
pr = NP.power(pr,0.001)
plt_pp  = [] 
plt_hf  = [] 
plt_hg  = [] 

p = pt
for i in range (1000):
    
    hf = CP.PropsSI ('H','P',p,'Q',0.0,fluid) / 1000.0
    hg = CP.PropsSI ('H','P',p,'Q',1.0,fluid) / 1000.0
    #ofile.write ('\t%10.2f \t%10.2f \t%10.2f \n' % (h,sf,sg))
    p = p * pr
    plt_pp.append (p)
    plt_hf.append (hf)
    plt_hg.append (hg)
#ofile.close()
title = 'T-s saturation line for : ' + fluid
plt.plot (plt_hf, plt_pp)
plt.plot (plt_hg, plt_pp)
plt.plot(plt_hc,plt_pc,'ro-')



for i in range(3):
    
    h_i = [nodes[i].h/1000, nodes[i+4].h/1000]
    p_i = [nodes[i].p, nodes[i+4].p]
    plt.plot(h_i,p_i,'--')



plt.xlabel('Enthalpy (kJ/kg)')
plt.ylabel('log(P/Pa)')
plt.yscale('log')
plt.title (title)
plt.show()  


