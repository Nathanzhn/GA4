import CoolProp.CoolProp as CP
import numpy as NP


def r_diagram():

    #ofile = open ('sat.txt','w')
    #fluid = input ('Enter fluid name: ')
    fluid = 'R134a'

    pc = CP.PropsSI(fluid, 'pcrit')
    pt = CP.PropsSI(fluid, 'ptriple')

    # Create lists of properties on saturation line with GP variation in p

    pr = (0.9999 * pc / pt)
    pr = NP.power(pr, 0.001)
    plt_TT = []
    plt_sf = []
    plt_sg = []
    plt_pp = []
    plt_hf = []
    plt_hg = []

    p = pt
    #ofile.write ('\t P (Pa) \t T (deg C) \t sf (kJ/kg.K) \t sg (kJ/kg.K) \t hf (kJ/kg.K) \t hg (kJ/kg.K)\n')
    for i in range(1000):
        TT = CP.PropsSI('T', 'P', p, 'Q', 0.0, fluid) - 273.15
        sf = CP.PropsSI('S', 'P', p, 'Q', 0.0, fluid) / 1000.0
        sg = CP.PropsSI('S', 'P', p, 'Q', 1.0, fluid) / 1000.0
        hf = CP.PropsSI('H', 'P', p, 'Q', 0.0, fluid) / 1000.0
        hg = CP.PropsSI('H', 'P', p, 'Q', 1.0, fluid) / 1000.0
        #ofile.write ('\t%10.2f \t%10.2f \t%10.2f \t%10.2f \t%10.2f \t%10.2f \n' % (p,TT,sf,sg,hf,hg))
        p = p * pr
        plt_TT.append(TT)
        plt_sf.append(sf)
        plt_sg.append(sg)
        plt_pp.append(p)
        plt_hf.append(hf)
        plt_hg.append(hg)

    # ofile.close()
    plt_TT = plt_TT[600:]
    plt_pp = plt_pp[600:]
    plt_sf = plt_sf[600:]
    plt_sg = plt_sg[600:]
    plt_hf = plt_hf[600:]
    plt_hg = plt_hg[600:]

    plt_TT += plt_TT[::-1]
    plt_pp += plt_pp[::-1]
    plt_sfg = plt_sf + plt_sg[::-1]
    plt_hfg = plt_hf + plt_hg[::-1]

    return plt_pp, plt_hfg, plt_TT, plt_sfg
