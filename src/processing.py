# %%
import numpy as np
from functions import * 
from config_sim import * 
# import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, title
import glob
import os
import pandas as pd
from datetime import datetime

# ## carga de la serie de datos
if DEBUG: print("loading data debugging:", DEBUG)
series_files = glob.glob(os.path.join(os.getcwd() , "data/series/*.csv"))

for filename in series_files:
    a_serie = pd.read_csv(f"./data/series/{os.path.basename(filename)}", decimal='.', delimiter=',', header=None, names=["serie"])
    serie_without_nan = a_serie["serie"].dropna().to_numpy().reshape(-1, 1)  ## remove NAs
    serie_mean = serie_without_nan ### media
    serie_sd = np.std(serie_without_nan)   ## sd
    data_serie = (a_serie - serie_without_nan.mean()) / np.std(serie_without_nan)

    n = len(serie_without_nan)
    # Probabilidad de ser punto de cambio para cada punto de la serie (0.01)
    Pi = np.concatenate([np.array([1.00]), np.repeat(0.01, n-1)], axis=0)
    data_fnct = pd.read_csv(
        f'./data/basis/Fmatrix-{os.path.basename(filename)}',
        decimal='.', delimiter=','
    ) 
    Fmatrix = np.array(data_fnct)
    
    # Probabilidad que una funcion sea seleccionada
    eta = np.concatenate([[1], np.repeat(0.01, Fmatrix.shape[1]-1)])

    print(
        f'./data/series/{os.path.basename(filename)}', a_serie.shape,
        f'./data/basis/Fmatrix-{os.path.basename(filename)}', Fmatrix.shape,
        f"output-{os.path.basename(filename)}"
    )
    
    start=datetime.now()
    if DEBUG: print(f"started at = {str(start)}")

    result_ = dbp_with_function_effect( Fmatrix, np.array(serie_without_nan), itertot, burnin, lec1, lec2,
                    nbseginit, nbfuncinit, nbtochangegamma, nbtochanger, Pi, eta,
                    threshold_bp, threshold_fnc, printiter=False,
                    fmatrixNames=list(data_fnct.columns), completeSerie=np.array(a_serie),
                    fileName=f"output-{os.path.basename(filename)}", ouputfolder="./data/outputs"
                    )
    
    crono = datetime.now() - start
    if DEBUG: print(f"ended at = { crono/60 }\n")   

    resMH = result_[0]
    # Puntos de cambio segn umbral
    breakpoints_bp = np.where(resMH["sumgamma"]/(itertot-burnin) > threshold_bp)[0]

    print("breakpoints_bp ", breakpoints_bp)
    # translations = translation(np.array(a_serie))
    # breakpoints_bp = [translations[val] for val in breakpoints_bp]
    if DEBUG: print("breakpoints_bp translated", breakpoints_bp)
# %%
