import states
from conditions import *
import CoolProp.CoolProp as CP
import numpy as np


class Compressor():

    # compressor component
    def __init__(self, inletstate, outletstate):
        "init compressor with state"
        self.inletstate = inletstate
        self.outletstate = outletstate

    def energy_simulate(self, state):

        self.eta = eta_c
        s_2s = state[self.inletstate].s
        h_2s = CP.PropsSI(
            'H', 'P', state[self.outletstate].p, 'S', s_2s, fluid)
        state[self.outletstate].h = state[self.inletstate].h +\
            (h_2s-state[self.inletstate].h)/self.eta
        state[self.outletstate].cal()

        self.w_c = (state[self.outletstate].h - state[self.inletstate].h)

    def exergy_simulate(self, state):
        self.w_comp = mdot_r*self.w_c
        self.DE = mdot_r*(state[self.outletstate].h - state[self.inletstate].h
                          - T0*(state[self.outletstate].s-state[self.inletstate].s))
        self.loss = mdot_r*T0 * \
            (state[self.outletstate].s-state[self.inletstate].s)


class Condensor():

    # condensor component
    def __init__(self, inletstate, outletstate):
        # init condensor state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def energy_simulate(self, state):

        self.dp = state[self.inletstate].p-state[self.outletstate].p

        self.mdot_con = mdot_con
        self.T_con_out = T_con_out
        self.cp = CP.PropsSI('C', 'T', self.T_con_out, 'P', 200000, fluid_con)

        self.qh = state[self.inletstate].h - state[self.outletstate].h
        self.T_con_in = self.T_con_out - mdot_r*self.qh/(self.mdot_con*self.cp)

    def exergy_simulate(self, state):

        ds = CP.PropsSI('S', 'T', self.T_con_out, 'P', 200000, fluid_con) - \
            CP.PropsSI('S', 'T', self.T_con_in, 'P', 200000, fluid_con)

        self.DE = mdot_r*((state[self.outletstate].h - state[self.inletstate].h) -
                          T0*(state[self.outletstate].s-state[self.inletstate].s))
        self.con_de = self.mdot_con * \
            (self.cp*(self.T_con_out-self.T_con_in)-T0*(ds))
        self.loss = -self.DE-self.con_de


class Throttle():

    # throttle component
    def __init__(self, inletstate, outletstate):
        # init throttle state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def energy_simulate(self, state):
        
        state[self.inletstate].cal()
        state[self.outletstate].h = state[self.inletstate].h
        state[self.outletstate].cal()

    def exergy_simulate(self, state):

        self.DE = mdot_r*((state[self.outletstate].h-state[self.inletstate].h)
                          - T0*(state[self.outletstate].s-state[self.inletstate].s))
        self.loss = mdot_r*T0 * \
            (state[self.outletstate].s - state[self.inletstate].s)


class Evaporator():
    # evaporator component
    def __init__(self, inletstate, outletstate):
        # init evaporator state
        self.inletstate = inletstate
        self.outletstate = outletstate

    def energy_simulate(self, state):

        state[self.inletstate].xx = True

        state[self.outletstate].t = T1
        self.dp = pf_eva*state[self.inletstate].p
        state[self.outletstate].p = state[self.inletstate].p - self.dp
        state[self.outletstate].cal()

        self.qc = state[self.outletstate].h - state[self.inletstate].h
        self.cp = CP.PropsSI('C', 'T', T_eva_in, 'P', 101500, fluid_eva)
        self.mdot_eva = mdot_eva
        self.T_eva_in = T_eva_in
        self.T_eva_out = self.T_eva_in-(mdot_r*self.qc)/(self.mdot_eva*self.cp)

    def exergy_simulate(self, state):

        self.DE = mdot_r*((state[self.outletstate].h-state[self.inletstate].h)
                          - T0*(state[self.outletstate].s-state[self.inletstate].s))
        self.eva_de = self.mdot_eva * \
            (self.cp*(self.T_eva_out-T_eva_in)-T0 *
             (self.cp*np.log(self.T_eva_out/self.T_eva_in)))
        self.loss = -self.DE-self.eva_de
