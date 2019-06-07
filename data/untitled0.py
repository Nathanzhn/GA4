import numpy as np
from matplotlib import pyplot as plt



plt_pp,plt_TT,plt_sf,plt_sg,plt_hf,plt_hg =np.loadtxt('sat.txt', skiprows=1, unpack=True)

fig, axs = plt.subplots(1,2,figsize=(16,6))
axPH = axs[0]
axTS = axs[1]
axPH.plot(plt_hf,plt_pp)
axPH.plot(plt_hg,plt_pp)
axPH.set_title("p-h Diagram for : " + fluid)
axPH.set_yscale("log")
axPH.set_xlabel("Enthalpy (kJ/kg)")
axPH.set_ylabel('log(P/Pa)')
axTS.plot(plt_sf,plt_TT)
axTS.plot(plt_sg,plt_TT)
axTS.set_title("T-s Diagram for : " + fluid)
axTS.set_xlabel("Specific entropy (kJ/(K.kg))")
axTS.set_ylabel('Temperature (deg. C)')





