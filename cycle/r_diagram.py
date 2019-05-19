import CoolProp.CoolProp as CP
import numpy as NP

def r_diagram():


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
    plt_pp  = [] 
    plt_hf  = [] 
    plt_hg  = [] 

    p = pt
    for i in range (1000):
        TT = CP.PropsSI ('T','P',p,'Q',0.0,fluid) - 273.15
        sf = CP.PropsSI ('S','P',p,'Q',0.0,fluid) / 1000.0
        sg = CP.PropsSI ('S','P',p,'Q',1.0,fluid) / 1000.0
        hf = CP.PropsSI ('H','P',p,'Q',0.0,fluid) / 1000.0
        hg = CP.PropsSI ('H','P',p,'Q',1.0,fluid) / 1000.0
        #ofile.write ('\t%10.2f \t%10.2f \t%10.2f \n' % (h,sf,sg))
        p = p * pr
        plt_TT.append(TT)
        plt_sf.append(sf)
        plt_sg.append(sg)
        plt_pp.append(p)
        plt_hf.append(hf)
        plt_hg.append(hg)
    
    #ofile.close()
    
    return plt_pp,plt_hf,plt_hg,plt_TT,plt_sf,plt_sg