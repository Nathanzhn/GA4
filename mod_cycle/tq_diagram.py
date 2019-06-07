import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
from conditions import * 
#from states import *
#from component import *
from cycle import *

def tq_diagram(states,hx):
    """ plot TQ Diagram"""
    
    #water side
    Tw = np.linspace(Tw_in,Tw_out,1000)
    cp_w = hx.cp_w
    Qw = mdot_w*cp_w*(Tw-Tw_in)
    
    #R134a side
    T_2 = states[1].t
    T_3 = states[2].t
    P2 = states[1].p
    P3 = states[2].p
    Pr = np.linspace(P3,P2,1000)
    h2 = states[1].h
    h3 = states[2].h
    hr = np.linspace(h3,h2,1000)
    mdot_rr = mdot_w*cp_w*(Tw_out-Tw_in)/(h2-h3)

    Tr = []
    Sr = []
    for i in range(len(hr)):
        tr = CP.PropsSI('T','P',Pr[i],'H',hr[i],fluid)
        sr = CP.PropsSI('S','P',Pr[i],'H',hr[i],fluid)/1000
        Tr.append(tr)
        Sr.append(sr)
    Qr = mdot_rr*(hr-h3)
    
    
    
    plt.plot(Qw,Tw)
    plt.plot(Qr,Tr)
    
    plt.xlabel('Q/(J/s)')
    plt.ylabel('T/K')
    ylim(310, 360)
    plt.show()
    

tq_diagram(states,b)