from Nodes import *
from compressor import *
from condensor import *
from throttle import *
from evaporator import *
from exp import *
from r_diagram import *

import matplotlib.pyplot as plt

fluid = 'R134a'



#0-3 Exp nodes, 4-7 Ideal nodes
nodes = [Node() for i in range(7)]
nodes[0].p = p1
nodes[0].t = T1
nodes[1].p = p2
nodes[1].t = T2
nodes[2].t = T3
nodes[3].t = T4

"these assumptions are embedded in components, but can be set in the main function as well"
""" #assumption in Exp components
nodes[2].x = 0.0 # condenser ideal state at outlet is saturated liquid 
nodes[3].h = nodes[2].h #throttle isenthalpic process """

""" # assumption in ideal components
nodes[5].s = nodes[1].s # compressor isentropic process
nodes[6].x = 0.0 # condenser ideal state at outlet is saturated liquid 
nodes[6].p = nodes[1].p # condenser p3=p2, no pressure loss
nodes[7].p = nodes[0].p # evaporator p4 = p1, no pressure loss
nodes[7].h = nodes[2].h #throttle isenthalpic process """

# Connect device
c = Compressor(0, 1, 4)
d = Condensor(1, 2, 5)
t = Throttle(2, 3, 6)
e = Evaporator(3,0, 6)


# simulate cycle and compute system properties
c.simulate(nodes)    
d.simulate(nodes,mdot_w,4200,Tw_in,Tw_out) 
t.simulate(nodes)      
e.simulate(nodes,mdot_a,1100,Ta_in,Ta_out)
print(e.mdot_r)

""" Carnot COP = T_h/(T_h-T_c)
inner COP = (h2-h3)/(h2-h1)
outer COP = mdot_w*shc*(Tw_out-Tw_in)/W_in """

#print(nodes[2].p)
#    myobj = attributes = [attr for attr in dir(nodes[2]) if not attr.startswith('__')]


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

axPH.plot(plt_hc,plt_pc,'ro-')
axTS.plot(plt_sc,plt_tc,'ro-')

# Plot ideal component nodes
for i in range(3):
    h_i = [nodes[i].h/1000, nodes[i+4].h/1000]
    p_i = [nodes[i].p, nodes[i+4].p]
    s_i = [nodes[i].s/1000, nodes[i+4].s/1000]
    t_i = [nodes[i].t-273.15, nodes[i+4].t-273.15]    
    axPH.plot(h_i,p_i,'--')
    axTS.plot(s_i,t_i,'--')

plt.show()  


