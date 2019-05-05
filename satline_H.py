#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 16:44:26 2019

@author: hz325
"""

#!/usr/local/apps/anaconda3-5.3.1/bin/python
#
# Script to plot the saturation line of a fluid
#
###############################################################
# Import the CoolProp property evaluation and plotting modules

import CoolProp.CoolProp as CP
import numpy as NP
import matplotlib.pyplot as PL

# Read in fluid name and calculate critical and triple point pressures

#ofile = open ('sat.out','w')

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

#ofile.write ('\t T (deg C) \t sf (kJ/kg.K) \t sg (kJ/kg.K)\n')
for i in range (1000):
    
    hf = CP.PropsSI ('H','P',p,'Q',0.0,fluid) / 1000.0
    hg = CP.PropsSI ('H','P',p,'Q',1.0,fluid) / 1000.0
    #ofile.write ('\t%10.2f \t%10.2f \t%10.2f \n' % (h,sf,sg))
    p = p * pr
    plt_pp.append (p)
    plt_hf.append (hf)
    plt_hg.append (hg)
#ofile.close()
title = 'H-s saturation line for : ' + fluid
PL.plot (plt_hf, plt_pp)
PL.plot (plt_hg, plt_pp)
PL.yscale('log')
PL.xlabel('Enthalpy (kJ/kg)')
PL.ylabel('log(P/Pa)')
PL.title (title)
PL.show()
