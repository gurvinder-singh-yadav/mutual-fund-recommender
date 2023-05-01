from src.api_helper import get_news_data, get_market_news_data
import os
import pandas as pd
import yfinance as yf
import datetime
from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import json


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
    symbol = data["Symbol"].tolist()[0]
    data = data.values[0]
    data = data.tolist()
    response.update(dict(zip(df.columns, data)))
    with open("data/yf_stock_info.json", "r") as f:
        js = json.load(f)
        js = js[symbol]
        response.update(js)
    return response

@app.get("/top_10_volume_tick")
async def top_10_volume_tick():
    today = str(datetime.date.today())
    path = os.path.join("data/tick/", today,"funds", "Ticker.csv")
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

@app.get("/marketnews")
async def get_market_news():
    return get_market_news_data()


def changer1(now):
    return int(now.value/1e6)
def changer2(val):
    return int(val)
def changer3(val):
    return val.strftime('%Y-%m-%d')
def changer4(val):
    temp = []
    for time,value in val:
        temp.append({"time":time,"value":value})
    return temp
def get_price(name):
    ticker = yf.Ticker(name)
    
    history = ticker.history("1mo")
    more_info = ticker.info
    t1 = list(history.index)
    t2 = list(history.Close)
    t3 = list(map(changer1,t1))
    t4 = list(map(changer3,t1))
    t5 = list(map(changer2, t2))
    t6 = list(zip(t3,t5))
    t7 = changer4(list(zip(t4,t5)))
    return t6,t7,more_info

@app.get("/get_yf")
async def get_yf(name: str):
    format1,format2,more_info = await get_price(name)
    return {"price_data":format1,"price_data_2": format2,"more_info": more_info}

@app.get("/parent_funds")
async def get_parent_funds(stock: str, n: int = 5):
    today = str(datetime.date.today())
    df = pd.read_csv("data/grow/{}/funds.csv".format(today))
    df = df[df["Name"] == stock]
    return df["funds_name"].iloc[:n].tolist()


@app.get("/parent_investor")
async def get_parent_investor(name: str, n: int = 5):
    today = str(datetime.date.today())
    df = pd.read_csv("data/tick/{}/funds/Ticker.csv".format(today))
    df = df[df["1"] == name]
    res = df["8"].tolist()[:n]
    return res


@app.get("/nifty")
async def get_nifty():
    format1,format2,more_info = await get_price("^NSEI")
    return {"price_data":format1,"price_data_2": format2,"more_info": more_info}