
import pandas as pd
import glob
import os

for variance in ["05"]:
    for miss in ["5", "10", "15", "20"]:
         path = "/Users/cristiangarcia/Desktop/missingness-influence/data/"
         with open(f"{path}/outputs/simulated-{miss}-{variance}-bf.csv", 'a') as bffl, \
            open(f"{path}/outputs/simulated-{miss}-{variance}-bp.csv", 'a') as bpfl:

            bffiles = glob.glob(os.path.join(path , f"raw/output-simulated-{miss}-*-{variance}.csv-bf.csv"))
            for filename in bffiles:
                df = pd.read_csv(filename, index_col=None, header=0)
                bffl.write(f"{', '.join(df.columns.values)}\n")
            
            bpfiles = glob.glob(os.path.join(path , f"raw/output-simulated-{miss}-*-{variance}.csv-bp.csv"))
            for filename in bpfiles:
                df = pd.read_csv(filename, index_col=None, header=0)
                bpfl.write(f"{', '.join(df.columns.values)}\n")