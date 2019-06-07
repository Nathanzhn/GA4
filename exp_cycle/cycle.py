from states import *
from component import *
from conditions import *
from r_diagram import *
import matplotlib.pyplot as plt
from pylab import *

# Numbering states
#For Exp cycle 0-3 Exp states, 4-7 Ideal states
states = [State() for i in range(7)]


## Assign conditions to states
#Exp conditions
states[0].p = p1
states[0].t = T1
states[1].p = p2
states[1].t = T2
states[2].t = T3
states[3].t = T4

#Ideal/Example paper conditions
#states[0].p = p1
#states[0].x = 1.0
#states[1].p = p2


# Connect device by relating their inlets and outlet state
#Exp connections
a = Compressor(0, 4, 1)
b = Condensor(1, 5, 2)
c = Throttle(2, 6, 3)
d = Evaporator(3,6, 0)

## Ideal/Example paper connnections
#a = Compressor(0, 1)
#b = Condensor(1, 2)
#c = Throttle(2, 3)
#d = Evaporator(3, 0)


# simulate cycle and compute system properties
a.simulate(states)    
b.simulate(states,mdot_w,4200,Tw_in,Tw_out) 
c.simulate(states)      
d.simulate(states,mdot_a,1100,Ta_in,Ta_out)

# sum up the component parameters
com_para = [a, b, c, d]


# Compute COP
T_h = (states[1].t +states[2].t)/2
T_c = (states[0].t +states[3].t)/2
COP_carnot = T_h/(T_h-T_c)
#COP_carnot = states[2].t/(states[2].t-states[0].t)
COP_inner = (states[1].h-states[2].h)/(states[1].h-states[0].h)
COP_outer = mdot_w*4200*(Tw_out-Tw_in)/a.w_c








#
#
#
## Set up saturation lines for ph and Ts diagrams
#plt_pp,plt_hfg,plt_TT,plt_sfg = r_diagram()
#fig, axs = plt.subplots(1,2,figsize=(16,6))
#axPH = axs[0]
#axTS = axs[1]
#axPH.plot(plt_hfg,plt_pp,'k')
#
#axPH.set_title("p-h Diagram for : " + fluid)
#axPH.set_yscale("log")
#axPH.set_xlabel("Enthalpy (kJ/kg)")
#axPH.set_ylabel('log(P/Pa)')
#axTS.plot(plt_sfg,plt_TT,'k')
#
#axTS.set_title("T-s Diagram for : " + fluid)
#axTS.set_xlabel("Specific entropy (kJ/(K.kg))")
#axTS.set_ylabel('Temperature (deg. C)')
#
## Plot cycle states
#plt_hc = [states[i].h/1000.0 for i in range(4)]
#plt_pc = [states[i].p for i in range(4)]
#plt_sc = [states[i].s/1000.0 for i in range(4)]
#plt_tc = [(states[i].t-273.15) for i in range(4)]
#
#plt_hc.append(states[0].h/1000.0)
#plt_pc.append(states[0].p)
#plt_sc.append(states[0].s/1000.0)
#plt_tc.append(states[0].t-273.15)
#
#axPH.plot(plt_hc,plt_pc,'ro--')
#axTS.plot(plt_sc,plt_tc,'ro--')
#axPH.text(states[0].h/1000.0, states[0].p - 2e5, '1', color='r')
#axPH.text(states[1].h/1000.0+10, states[1].p , '2', color='r')
#axPH.text(states[2].h/1000.0-10, states[2].p + 2e5, '3', color='r')
#axPH.text(states[3].h/1000.0-10, states[3].p - 2e5, '4', color='r')
#
#axTS.text(states[0].s/1000.0+0.05, states[0].t - 273.15, '1', color='r')
#axTS.text(states[1].s/1000.0+0.05, states[1].t - 273.15, '2', color='r')
#axTS.text(states[2].s/1000.0-0.05, states[2].t + - 273.15, '3', color='r')
#axTS.text(states[3].s/1000.0-0.05, states[3].t - 273.15-5, '4', color='r')
#
## Plot ideal component states
#if a.idealoutletstate:
#    for i in range(3):
#        h_i = [states[i].h/1000, states[i+4].h/1000]
#        p_i = [states[i].p, states[i+4].p]
#        s_i = [states[i].s/1000, states[i+4].s/1000]
#        t_i = [states[i].t-273.15, states[i+4].t-273.15]    
#        axPH.plot(h_i,p_i,'b.-')
#        axTS.plot(s_i,t_i,'b.-')
#else:
#    pass
#
#plt.show()  
#

