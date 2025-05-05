# -*- coding: utf-8 -*-
# Load libraries
# %%
import numpy as np
# import matplotlib
from datetime import datetime
from generator import generator
from missingness import *

############### simular serie

# %%
# 1 serie with 4 segments, with a functional part, 100 points. We 
# one variance for the error term.
M = 1
n = 100 
K = 4
sigma_ = 0.5 # (0.1,0.5, 1, 1.5) Plantear el mismo escenario del paper

# %%
muChoix = np.array([0, 1, 2, 3, 4, 5])
standard_deviation = np.array([sigma_])
varianceError = np.power(standard_deviation, 2)
pHaar = np.array([10, 50, 60])
p1 = 3
p2 = 5
nbsimu = 1
series = generator(M, n, K, muChoix, varianceError, pHaar, p1, p2)

# %%
# Obtaining the serie 
data_serie = np.array((series[5]["mu"] + series[5]["biais"] + series[5]["erreur1"]))
np.savetxt(f"data/series/simlated-ground-truth.csv", data_serie, delimiter=",")

# %%
for percent in [5, 10, 15, 20]:
    for idx in np.arange(0, 100, 1, dtype=int):
        na_serie = mcar_method(data_serie, percentage=percent, seed=idx)
        np.savetxt(f"data/series/simulated-{percent}-{idx}-05.csv", na_serie, delimiter=",")

#%%
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
plt.plot(data_serie, marker='o')

# %%
