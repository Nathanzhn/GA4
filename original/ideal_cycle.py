from Nodes import *
from component import *
from exp_ideal import *
from r_diagram import *

import matplotlib.pyplot as plt

fluid = 'R134a'

#0-3 Exp nodes, 4-7 Ideal nodes
nodes = [Node() for i in range(7)]
nodes[0].p = p1
nodes[0].t = T1
nodes[1].p = p2


# Connect device
a = Compressor(0, 1, 1)
b = Condensor(1, 2, 2)
c = Throttle(2, 3, 3)
d = Evaporator(3,0, 3)


# simulate cycle and compute system properties
a.simulate(nodes)    
b.simulate(nodes,mdot_w,4200,Tw_in,Tw_out) 
c.simulate(nodes)      
d.simulate(nodes,mdot_a,1100,Ta_in,Ta_out)
com_para = [a, b, c, d]
#print(a.eta)




# Set up saturation lines for ph and Ts diagrams
plt_pp,plt_hf,plt_hg,plt_TT,plt_sf,plt_sg = r_diagram()
fig, axs = plt.subplots(1,2,figsize=(16,6))
axPH = axs[0]
axTS = axs[1]
axPH.plot(plt_hf,plt_pp)
axPH.plot(plt_hg,plt_pp)
axPH.set_title("p-h Diagram for : " + fluid)
axPH.set_yscale("log")
axPH.set_xlabel("Enthalpy (kJ/kg)")
axPH.set_ylabel('log(P/Pa)')
axTS.plot(plt_sf,plt_TT)
axTS.plot(plt_sg,plt_TT)
axTS.set_title("T-s Diagram for : " + fluid)
axTS.set_xlabel("Specific entropy (kJ/(K.kg))")
axTS.set_ylabel('Temperature (deg. C)')


# Plot exp nodes
plt_hc = [nodes[i].h/1000.0 for i in range(4)]
plt_pc = [nodes[i].p for i in range(4)]
plt_sc = [nodes[i].s/1000.0 for i in range(4)]
plt_tc = [(nodes[i].t-273.15) for i in range(4)]

plt_hc.append(nodes[0].h/1000.0)
plt_pc.append(nodes[0].p)
plt_sc.append(nodes[0].s/1000.0)
plt_tc.append(nodes[0].t-273.15)

