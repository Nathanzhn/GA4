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
    cp_w = 4200
    Qw = mdot_w*cp_w*(Tw-Tw_in)
    
    #R134a side
    T_2 = states[1].t
    T_3 = states[2].t
    P2 = states[1].p
    P3 = states[2].p
    Pr = np.linspace(P2,P3,1000)
    h2 = states[1].h
    h3 = states[2].h
    hr = np.linspace(h2,h3,1000)
    mdot_rr = mdot_w*cp_w*(Tw_out-Tw_in)/(h2-h3)
    Tr = CP.PropsSI('T','P',Pr,'H',hr,fluid)
    Sr = CP.PropsSI('S','P',Pr,'H',hr,fluid)
    sdt = 0
    for i in range(len(hr)-1):
        sdt += mdot_rr*(hr[i+1]-hr[i])/Tr[i+1] +(Qw[i+1]-Qw[i])/Tw[i+1]
        i +=1
        
    Qr = mdot_rr*(hr-h3)
    loss_dt = sdt*T0
    sw_out = CP.PropsSI('S','T',Tw_out,'P',200000,'water')
    sw_in = CP.PropsSI('S','T',Tw_in,'P',200000,'water')
    
    loss_tt = -mdot_rr*(states[2].h-states[1].h-T0*(states[2].s-states[1].s))-mdot_w*(cp_w*(Tw_out-Tw_in)-T0*(sw_out-sw_in))
    

    plt.plot(Qw,Tw)
    plt.plot(Qr,Tr)
    
    plt.xlabel('Q/(J/s)')
    plt.ylabel('T/K')
    ylim(310, 360)
    plt.show()
    
    return loss_dt,loss_tt
    
if __name__ == "__main__":
    gg,tt = tq_diagram(states,b)
    print(gg)
    print(tt)