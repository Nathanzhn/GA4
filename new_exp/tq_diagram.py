import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
from conditions import * 
import numpy as np
#from states import *
#from component import *
#from cycle import *

def tq_diagram_con(states,hx,fluid_ext,mdot_ext,T_ext_in,T_ext_out):
    """ plot TQ Diagram"""
    
    #ext side
    T_ext = np.linspace(T_ext_in,T_ext_out,1000)
    cp = hx.cp
    Q_ext = mdot_ext*cp*(T_ext-T_ext_in)
        
    #R134a side
    T_2 = states[1].t
    T_3 = states[2].t
    P2 = states[1].p
    P3 = states[2].p
    Pr = np.linspace(P2,P3,1000)
    h2 = states[1].h
    h3 = states[2].h
    hr = np.linspace(h2,h3,1000)
    mdot_rr = mdot_ext*cp*(T_ext_out-T_ext_in)/(h2-h3)
    Tr = CP.PropsSI('T','P',Pr,'H',hr,fluid)
    Sr = CP.PropsSI('S','P',Pr,'H',hr,fluid)
    sdt = 0
    for i in range(len(hr)-1):
        sdt += mdot_rr*(hr[i+1]-hr[i])/Tr[i+1] +(Q_ext[i+1]-Q_ext[i])/T_ext[i+1]
        i +=1
     
    loss_dt = sdt*T0            
    Qr = mdot_rr*(hr-h3)
    
    s_ext_out = CP.PropsSI('S','T',T_ext_out,'P',200000,fluid_ext)
    s_ext_in = CP.PropsSI('S','T',T_ext_in,'P',200000,fluid_ext)
    loss_tt = -mdot_rr*(states[2].h-states[1].h-T0*(states[2].s-states[1].s))-mdot_ext*(cp*(T_ext_out-T_ext_in)-T0*(s_ext_out-s_ext_in))
    loss_dp = loss_tt - loss_dt
    
    plt.plot(Q_ext,T_ext)
    plt.plot(Qr,Tr)
    
    plt.xlabel('Q/(J/s)')
    plt.ylabel('T/K')
    plt.ylim(310, 360)
    plt.show()
    
    return loss_dt,loss_tt


def tq_diagram_eva(states,hx,fluid_ext,mdot_rr,T_ext_in,T_ext_out):
    """ plot TQ Diagram"""
    

    
    #R134a side
    T_1 = states[0].t
    T_4 = states[3].t
    P1 = states[0].p
    P4 = states[3].p
    Pr = np.linspace(P4,P1,1000)
    h1 = states[0].h
    h4 = states[3].h
    hr = np.linspace(h4,h1,1000)

    
    #ext side
    T_ext = np.linspace(T_ext_in,T_ext_out,1000)
    cp = hx.cp
    mdot_ext = mdot_rr*(h1-h4)/(cp*(T_ext_in-T_ext_out))
    Q_ext = mdot_ext*cp*(T_ext-T_ext_out)
    
    Tr = CP.PropsSI('T','P',Pr,'H',hr,fluid)
    Sr = CP.PropsSI('S','P',Pr,'H',hr,fluid)
    sdt = 0
    for i in range(len(hr)-1):
        sdt += mdot_rr*(hr[i+1]-hr[i])/Tr[i+1] +(Q_ext[i+1]-Q_ext[i])/T_ext[i+1]
        i +=1
     
    loss_dt = sdt*T0            
    Qr = mdot_rr*(hr-h4)

    loss_tt = -mdot_rr*((states[0].h-states[3].h)-T0*(states[0].s-states[3].s))\
                             -mdot_ext*(cp*(T_ext_out-T_ext_in)-T0*(cp*np.log(T_ext_out/T_ext_in)))
    loss_dp = loss_tt - loss_dt
    
    plt.plot(Q_ext,T_ext)
    plt.plot(Qr,Tr)
    
    plt.xlabel('Q/(J/s)')
    plt.ylabel('T/K')
#    plt.ylim(310, 360)
    plt.show()
    
    return loss_dt,loss_dp