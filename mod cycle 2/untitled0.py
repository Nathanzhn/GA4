# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 23:32:50 2019

@author: 82656
"""


# Set up saturation lines for ph and Ts diagrams
plt_pp,plt_hfg,plt_TT,plt_sfg = r_diagram()
fig, axs = plt.subplots(1,2,figsize=(12,4))
axPH = axs[0]
axTS = axs[1]
axPH.plot(plt_hfg,plt_pp,'k')

axPH.set_title("p-h Diagram for : " + fluid)
axPH.set_yscale("log")
axPH.set_xlabel("Enthalpy (kJ/kg)")
axPH.set_ylabel('log(P/Pa)')
axTS.plot(plt_sfg,plt_TT,'k')

axTS.set_title("T-s Diagram for : " + fluid)
axTS.set_xlabel("Specific entropy (kJ/(K.kg))")
axTS.set_ylabel('Temperature (deg. C)')

axPH.plot(exp_plt_hc,exp_plt_pc,'b--',mod_plt_hc,mod_plt_pc,'r--')
axTS.plot(exp_plt_sc,exp_plt_tc,'b--',mod_plt_sc,mod_plt_tc,'r--')
plt.show()  










