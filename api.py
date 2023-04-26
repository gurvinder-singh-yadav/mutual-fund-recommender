from src.scraper import save_summaries, concat, scrape_funds, get_tick_links,get_tick_funds
from src.api_helper import concat_grow_funds
import os
import pandas as pd
import datetime
from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()

class Stock:
    def __init__(self, name):
        self.name

@app.get("/")
async def root():
    return "you are in page"

@app.get("/top_10_volume_grow")
async def top_10_volume_grow():
    today = str(datetime.date.today())
    path = os.path.join("data/grow", today, "funds.csv")
    df = pd.read_csv(path)
    total_assets = df.groupby("Name").aggregate(sum).reset_index()[["Name", "Assets"]]
    total_assets = total_assets.sort_values("Assets", ascending=False)
    top_10 = total_assets.iloc[:10]["Name"].values.tolist()
    return top_10

def stock_info_fn(stock_name):
    df = pd.read_csv("data/stock_info.csv")
    data = df[df["name"] == stock_name]
    response = {}
    data = data.values[0]
    data = data.tolist()
    response.update(dict(zip(df.columns, data)))
    return response

@app.get("/stock_info/{stock_name}")
async def stock_info(stock_name):
    df = pd.read_csv("data/stock_info.csv")
    data = df[df["name"] == stock_name]
    response = {}
    data = data.values[0]
    data = data.tolist()
    response.update(dict(zip(df.columns, data)))
    return response
