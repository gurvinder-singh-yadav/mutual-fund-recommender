from src.scraper import save_summaries, concat, scrape_funds, get_tick_links,get_tick_funds
from src.api_helper import concat_grow_funds, get_news_data
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
@app.get("/top_10_volume_tick")
async def top_10_volume_tick():
    today = str(datetime.date.today())
    path = os.path.join("data/tick/", today,"fundst", "Ticker.csv")
    df = pd.read_csv(path)
    total_assets = df.groupby("1").aggregate(sum).reset_index()[["1", "7"]]
    total_assets["7"] = total_assets["7"].astype('str')
    total_assets = total_assets.sort_values("7", ascending=False)
    top_10 = total_assets.iloc[:10]["1"].values.tolist()
    return top_10

@app.get("/news/{date}")
async def get_news(date):
    """
    date: format('2023-04-28')
    """
    return get_news_data(date)