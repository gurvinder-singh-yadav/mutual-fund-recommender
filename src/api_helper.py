from datetime import date
import shutil
import os
import pandas as pd
import glob
import datetime
import re

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


def get_news_data(date):
    df = pd.read_csv("data/news_process.csv")
    # return [date, df["date"].iloc[0]]
    df = df[df["date"] == date]

    # return df
    return df.to_dict("list")   

def convert_date(date: str):
    # print(date)
    format = "%b %d, %Y, %I:%M %p %Z"
    date = datetime.datetime.strptime(date, format)
    return date.strftime("%Y-%m-%d")   

def get_target_price(title):
    target_price = re.findall("\d+", title)
    try:
        target_price = int(target_price[0])
        return target_price
    except:
        return None 

def process_news():
    df = pd.read_csv("data/news.csv")
    df = df.dropna()
    df["target_price"] = df["title"].apply(get_target_price)
    df["buy/sell"] = df["title"].apply(lambda x: x.split(" ")[0])
    df["stock"] = df["title"].apply(lambda x: x.split(",")[0][4:])
    df["fund"] = df["title"].apply(lambda x: x.split(":")[-1])
    # df["date"] = df["time"].apply(convert_date)
    df["date"] = df["time"]
    del df["time"]
    df.to_csv("data/news_process.csv", index=None)