from src.api_helper import get_news_data
import os
import pandas as pd
import datetime
from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Stock:
    def __init__(self, name):
        self.name

@app.get("/")
async def root():
    return "you are in page"

@app.get("/top_volume_grow")
async def top_n_volume_grow(n: int = 10):
    today = str(datetime.date.today())
    path = os.path.join("data/grow", today, "funds.csv")
    df = pd.read_csv(path)
    total_assets = df.groupby("Name").aggregate(sum).reset_index()[["Name", "Assets(Rs_Cr.)"]]
    total_assets = total_assets.sort_values("Assets(Rs_Cr.)", ascending=False)
    top = total_assets["Name"].values.tolist()[:n]
    return top

@app.get("/most_pop_stocks")
async def most_pop_stocks(n: int = 10):
    today = str(datetime.date.today())
    path = os.path.join("data/grow", today, "funds.csv")
    df = pd.read_csv(path)
    total_assets = df.groupby("Name").count().reset_index()[["Name", "Assets(Rs_Cr.)"]]
    total_assets = total_assets.sort_values("Assets(Rs_Cr.)", ascending=False)
    top = total_assets["Name"].values.tolist()[:n]
    return top

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