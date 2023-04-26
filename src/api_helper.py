from datetime import date
import shutil
import os
import pandas as pd
import glob

def remove_percent_symbol(x):
    return x.rstrip("%")

def concat_grow_funds():
    today = str(date.today())
    today_dir = os.path.join("data","grow" ,today)
    funds_dir = os.path.join(today_dir, "funds")
    if os.path.exists(funds_dir):
        files = glob.glob(os.path.join(funds_dir, "*.csv"))
        dfs = []
        for file in files:
            dfs.append(pd.read_csv(file, index_col=None))
        shutil.rmtree(funds_dir)
        funds = pd.concat(dfs, ignore_index=True)
        funds["Assets"] = funds["Assets"].apply(remove_percent_symbol)
        funds.to_csv(os.path.join(today_dir, "funds.csv"), index = None)



        