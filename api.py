from src.scraper import save_summaries, concat, scrape_funds
from src.api_helper import concat_grow_funds
import os
import pandas as pd
import datetime
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/update_index_grow")
async def update_index_grow():
    save_summaries()
    today = str(datetime.date.today())
    concat("data/grow/{}/index".format(today))
    return "Updated"

@app.get("/")
async def root():
    return "you are in page"

@app.get("/update_funds_grow")
async def update_funds_grow():
    scrape_funds()
    concat_grow_funds()
    return "Done"

@app.get("/top_10_volume_grow")
async def top_10_volume_grow():
    today = str(datetime.date.today())
    path = os.path.join("data/grow", today, "funds.csv")
    df = pd.read_csv(path)
    total_assets = df.groupby("Name").aggregate(sum).reset_index()[["Name", "Assets"]]
    total_assets = total_assets.sort_values("Assets", ascending=False)
    top_10 = total_assets.iloc[:10]["Name"].values.tolist()
    return top_10

@app.get("/top_10_popular_grow")
async def top_10_popular_grow():
    today = str(datetime.date.today())
    path = os.path.join("data/grow", today, "funds.csv")
    df = pd.read_csv(path)
    asset_popularity = df.groupby("Name").count().reset_index()[["Name", "Assets"]]
    asset_popularity.sort_values(by="Assets", ascending=False)
    top_10 = asset_popularity.iloc[:10]["Name"].values.tolist()
    return top_10