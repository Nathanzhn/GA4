# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import CoolProp.CoolProp as CP
import numpy as NP
import matplotlib.pyplot as PL

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
PL.plot (plt_hf, plt_pp)
PL.plot (plt_hg, plt_pp)
""" PL.plot(plt_hc,plt_pc,'ro-') """

#PL.plot([h1/1000.0,h2/1000.0,h3/1000.0,h4/1000.0,h1/1000.0], [p1,p2,p3,p4,p1], "k", linewidth=2)
#print(h2/1000.0,p2,h3/1000.0,p3)
#PL.plot([p3,h3/1000.0], [p2,h2/1000.0], "k", linewidth=2)
#print(h2/1000.0,p2,h3/1000.0,p3)
#PL.plot([p3,h3/1000.0], [p4,h4/1000.0], "k", linewidth=2)
#PL.plot([p4,h4/1000.0], [p1,h1/1000.0], "k", linewidth=2)

PL.yscale('log')
PL.xlabel('Enthalpy (kJ/kg)')
PL.ylabel('log(P/Pa)')
PL.title (title)
PL.show()