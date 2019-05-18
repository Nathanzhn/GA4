# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:02:18 2019

@author: 82656
"""
import numpy as np
from matplotlib import pyplot as plt

time,TA,TB,TC,TD,T1,T2,T3,T4,Dp,P2,P1 = np.loadtxt('HP_May10_05.txt', skiprows=1, unpack=True)

Ext_T = np.vstack((TA,TB,TC,TD)).transpose()
R134a_T = np.vstack((T1,T2,T3,T4)).transpose()
R134a_P = np.vstack((P1,P2)).transpose()

fig, axs = plt.subplots(2,2,figsize=(12,10))

axTA = axs[0,0]
axT1 = axs[0,1]
axDP = axs[1,0]
axP1 = axs[1,1]




axTA.plot(time,TA,label='TA')
axTA.plot(time,TB,label='TB')
axTA.plot(time,TC,label='TC')
axTA.plot(time,TD,label='TD')
axT1.plot(time,T1,label='T1')
axT1.plot(time,T2,label='T2')
axT1.plot(time,T3,label='T3')
axT1.plot(time,T4,label='T4')
axDP.plot(time, Dp,label='Dp')
axP1.plot(time, P1,label='P1')
axP1.plot(time, P2,label='P2')



axi = ( {'ax':axTA,  'tit':'External Temperatures', 'ylab':'Temperature (C)'},
         {'ax':axT1, 'tit':'R134a Temperatures', 'ylab':'Temperature (C)'},
         {'ax':axDP, 'tit':'Flow pressure diff.', 'ylab':'Pressure (bar)'},
         {'ax':axP1, 'tit':'R134a Pressures', 'ylab':'Pressure (bar)'} )
    
    
for a in axi:
    a['ax'].set_xlabel('Time (s)')
    a['ax'].set_ylabel(a['ylab'])
    a['ax'].set_title(a['tit'])
    a['ax'].legend(loc='lower left')
    a['ax'].grid()        

plt.show()





