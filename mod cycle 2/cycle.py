from states import *
from component import *
from conditions import *
from r_diagram import *
from tq_diagram import tq_diagram_con, tq_diagram_eva
import matplotlib.pyplot as plt
from pylab import *
from prettytable import PrettyTable
import CoolProp.CoolProp as CP
import numpy as np

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})



# restate input conditions






def COP_f():
    
    # Numbering states
    #For Exp cycle 0-3 Exp states, 4-7 Ideal states
    states = [State() for i in range(4)]
    
    
    ## Assign conditions to states
    states[0].t = T1
    states[2].t = T3
    states[3].t = T4
    states[2].p = p3
    
    # Connect device by relating their inlets and outlet state
    a = Compressor(0, 1)
    b = Condensor(1, 2)
    c = Throttle(2, 3)
    d = Evaporator(3, 0)
    
    
    # simulate cycle and compute system properties
    c.energy_simulate(states) 
    states[1].p =  states[2].p/(1-pf_con)   
    d.energy_simulate(states)
    a.energy_simulate(states)    
    b.energy_simulate(states) 
    
    
    #exergy analysis
    a.exergy_simulate(states)    
    b.exergy_simulate(states) 
    c.exergy_simulate(states)      
    d.exergy_simulate(states)
    
    
    
    # sum up the component parameters
    com_para = [a, b, c, d]
    
    
    # Compute COP
    T_h = (states[1].t +states[2].t)/2
    T_c = (states[0].t +states[3].t)/2
    COP_carnot = T_h/(T_h-T_c)
    #COP_carnot = states[2].t/(states[2].t-states[0].t)
    COP_inner = (states[1].h-states[2].h)/(states[1].h-states[0].h)
    COP_outer = mdot_con*b.cp*(b.T_con_out-b.T_con_in)/w_tot

    return COP_carnot, COP_inner, COP_outer


#w_loss = w_tot-w_fan-a.w_comp
#
#
##exergy listing
#x = PrettyTable()
#
#x.field_names = ["exergy", "Value"]
#
#x.add_row(["compressor loss", a.loss])
#x.add_row(["Condenser", b.loss])
#x.add_row(["Throttle",c.loss])
#x.add_row(["Evaporator", d.loss])
#x.add_row(["wasted electrical power",w_loss])
#x.add_row(["total loss", a.loss+b.loss+c.loss+d.loss])
#x.add_row(["water",b.con_de])
#x.add_row(["air",d.eva_de])
#x.add_row(["comp",a.w_comp])
#x.add_row(["fan",w_fan])



##Compressor exergy
#x.add_row(["R134a de", a.DE])
#x.add_row(["w_comp", a.w_comp])
#x.add_row(["loss",a.loss])
#x.add_row(["sum",a.w_comp-a.loss-a.DE])
#
##Condenser exergy
#x.add_row(["R134a de", b.DE])
#x.add_row(["water de", b.con_de])
#x.add_row(["loss",b.loss])
#x.add_row(["sum",b.DE+b.con_de+b.loss])
#
##Compressor exergy
#x.add_row(["R134a de", c.DE])
#x.add_row(["loss",c.loss])
#x.add_row(["sum",c.DE+c.loss])
#
##Compressor exergy
#x.add_row(["R134a de", d.DE])
#x.add_row(["air de", d.eva_de])
#x.add_row(["loss",d.loss])
#x.add_row(["sum",d.DE+d.eva_de+d.loss])

#loss_dt_con,loss_tt_con = tq_diagram_con(states,b,fluid_con,mdot_con,b.T_con_in,b.T_con_out)
#x.add_row(["con loss dt", loss_dt_con])
#x.add_row(["con loss tt",loss_tt_con])
#
#
#loss_dt_eva,loss_tt_eva = tq_diagram_eva(states,d,fluid_eva,mdot_r,d.T_eva_in,d.T_eva_out)
#x.add_row(["eva loss dt", loss_dt_eva])
#x.add_row(["eva loss tt",loss_tt_eva])
#
#print(x)
#




##bar chart of exergy terms
#plt.rcdefaults()
#objects = ('work in', 'water', 'air', 'compressor loss', 'condenser loss', 'throttle loss', 'evaporator loss', 'fan power', 'electrical loss')
#y_pos = np.arange(len(objects))
#performance = np.round(np.array([w_tot,b.con_de,d.eva_de,a.loss,b.loss,c.loss,d.loss,w_fan,(w_tot-w_fan-a.w_comp)])/w_tot*100,decimals=1)
#for i, v in enumerate(performance):
#    text(v + 0.25, i , str(v)+'%', color='blue', fontweight='bold')
#
#
#
#plt.barh(y_pos,performance, align='center', alpha=0.5)
#plt.yticks(y_pos, objects)
#plt.xlabel('Usage')
#plt.title('Programming language usage')
#
#plt.show()

#
#print(mdot_con,mdot_r,d.mdot_eva)
#print(COP_carnot, COP_inner,COP_outer)
#
#


# Set up saturation lines for ph and Ts diagrams
#plt_pp,plt_hfg,plt_TT,plt_sfg = r_diagram()
#fig, axs = plt.subplots(1,2,figsize=(12,4))
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

# Plot cycle states

##curve between state 2,3

#mod_Pr = np.linspace(states[1].p,states[2].p,1000).tolist()
#mod_Hr = np.linspace(states[1].h,states[2].h,1000)
#mod_Tr = (CP.PropsSI('T','P',mod_Pr,'H',mod_Hr,fluid)-273.15).tolist()
#mod_Sr = (CP.PropsSI('S','P',mod_Pr,'H',mod_Hr,fluid)/1000).tolist()
#mod_Hr = (mod_Hr/1000).tolist()
#
#
#
#mod_plt_hc = [states[i].h/1000.0 for i in range(4)]
#mod_plt_pc = [states[i].p for i in range(4)]
#mod_plt_sc = [states[i].s/1000.0 for i in range(4)]
#mod_plt_tc = [(states[i].t-273.15) for i in range(4)]
#mod_plt_hc[2:2] = mod_Hr
#mod_plt_pc[2:2] = mod_Pr
#mod_plt_tc[2:2] = mod_Tr
#mod_plt_sc[2:2] = mod_Sr
#
#
#
#
#mod_plt_hc.append(states[0].h/1000.0)
#mod_plt_pc.append(states[0].p)
#mod_plt_sc.append(states[0].s/1000.0)
#mod_plt_tc.append(states[0].t-273.15)









#
#axPH.plot(mod_plt_hc,mod_plt_pc,'r--')
#axTS.plot(mod_plt_sc,mod_plt_tc,'r--')
#axPH.text(states[0].h/1000.0, states[0].p - 1e5, '1', color='r')
#axPH.text(states[1].h/1000.0+6, states[1].p , '2', color='r')
#axPH.text(states[2].h/1000.0-10, states[2].p + 1e5, '3', color='r')
#axPH.text(states[3].h/1000.0-10, states[3].p - 1e5, '4', color='r')
#
#axTS.text(states[0].s/1000.0+0.03, states[0].t - 273.15, '1', color='r')
#axTS.text(states[1].s/1000.0+0.03, states[1].t - 273.15, '2', color='r')
#axTS.text(states[2].s/1000.0-0.05, states[2].t - 273.15, '3', color='r')
#axTS.text(states[3].s/1000.0-0.05, states[3].t - 273.15-5, '4', color='r')
#
#
#
#plt.show()  


