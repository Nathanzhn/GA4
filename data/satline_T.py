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
plt_TT  = [] 
plt_sf  = [] 
plt_sg  = [] 

p = pt
#ofile.write ('\t T (deg C) \t sf (kJ/kg.K) \t sg (kJ/kg.K)\n')
for i in range (1000):
    TT = CP.PropsSI ('T','P',p,'Q',0.0,fluid) - 273.15
    sf = CP.PropsSI ('S','P',p,'Q',0.0,fluid) / 1000.0
    sg = CP.PropsSI ('S','P',p,'Q',1.0,fluid) / 1000.0
    #ofile.write ('\t%10.2f \t%10.2f \t%10.2f \n' % (TT,sf,sg))
    p = p * pr
    plt_TT.append (TT)
    plt_sf.append (sf)
    plt_sg.append (sg)
#ofile.close()
title = 'T-s saturation line for : ' + fluid
PL.plot (plt_sf, plt_TT)
PL.plot (plt_sg, plt_TT)
PL.xlabel('Specific entropy (kJ/K.kg)')
PL.ylabel('Temperature (deg. C)')
PL.title (title)
PL.show()
