from .scrapper import  scrape
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def db_create(k = 1):
    final = {}
    input_ = range(k)

    exe = ThreadPoolExecutor(max_workers=8)
    futures = exe.map(scrape,input_)
    for i in futures:
        final.update(i)
    data = []
    for k in final.keys():
        temp = {}
        for j in final[k]:
            data.append([k,j[0], j[1],float(j[-1].rstrip("%"))])
    return data


def db_save(data,name="data/file.csv"):
    df = pd.DataFrame(data)
    df.columns = ["Fund-name","invested-firm","industry","percentage"]
    df.to_csv(name, index=False)