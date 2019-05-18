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


p1=100000
p3=800000

#p1=1.0*p
#p3=20.0*p
efficiency=1








#state 1
p1 = p1
T1 = CP.PropsSI('T','P',p1,'Q',1.0,fluid)
h1 = CP.PropsSI('H','P',p1,'Q',1.0,fluid)
s1 = CP.PropsSI('S','P',p1,'Q',1.0,fluid)


#state 2
p2 = p3
h2s = CP.PropsSI('H','P',p2,'S',s1,fluid)
h2 = h1 +(h2s-h1)/efficiency
T2 = CP.PropsSI('T','P',p2,'H',h2,fluid)
s2 = CP.PropsSI('S','P',p2,'H',h2,fluid)

#state 2f
p2f = p2
T2f = CP.PropsSI('T','P',p2,'Q',1.0,fluid)
h2f = CP.PropsSI('H','P',p2,'Q',1.0,fluid)
s2f = CP.PropsSI('S','P',p2,'Q',1.0,fluid)



#state 3
p3=p3
T3 = CP.PropsSI('T','P',p3,'Q',0.0,fluid)
h3 = CP.PropsSI('H','P',p3,'Q',0.0,fluid)
s3 = CP.PropsSI('S','P',p3,'Q',0.0,fluid)


#state 4
p4=p1
h4=h3
T4 = CP.PropsSI('T','P',p4,'H',h4,fluid)
s4 = CP.PropsSI('S','P',p4,'H',h4,fluid)


# 1-2 compressor
wc = h2-h1 
# 2-3 condenser
qh = h2-h3
# 3-4 throttle
#h4=h3
# 4-1 evaporater
qc = h1-h4
#Coefficient of Performance
COP = qh/wc


h2r = []
p2r = []



h2r.append([h1/1000.0,h2/1000.0,h3/1000.0,h4/1000.0,h1/1000.0])
p2r.append([p1,p2,p3,p4,p1])
plt_pc = p2r
plt_hc = h2r





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
PL.plot(plt_hc,plt_pc,'ro-')

PL.plot([h1/1000.0,h2/1000.0,h3/1000.0,h4/1000.0,h1/1000.0], [p1,p2,p3,p4,p1], "k", linewidth=2)
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





