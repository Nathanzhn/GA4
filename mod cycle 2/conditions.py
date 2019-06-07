import numpy as np

# fluid parameters
fluid = 'R134a'
mdot_r = 0.030986220633539258 
fluid_con = 'water'
mdot_con = 0.10867275299737268
fluid_eva = 'air'
mdot_eva = 0.7242923014083904

# work parameters
w_fan = 164
w_tot = 1660
eta_e = 0.20158636238415156
eta_c = 0.67193222194797

# inner cycle parameters
dT14 = 0.8361774744027457 #superheat T at state 1
T3 = 51.98430034129692+273.15 #condenser T
T4 = 17.752559726962456+273.15 #Evaporator T
pf_con = 0.02420773780690382
pf_eva = 0.07427499588832076
T1 = dT14 +T4
p3 = 1595831.313754499


# condenser parameters
T_con_out = 57.00524934383202+273.15

# evaporator parameters
T_eva_in = 24.628608923884514+273.15
T0 = T_eva_in