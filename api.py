from src.scraper import save_summaries, concat, scrape_funds, get_tick_links,get_tick_funds
from src.api_helper import concat_grow_funds
import os
import pandas as pd
import datetime
from fastapi import FastAPI

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
    pass

@app.get("/update_ticker_index")
async def update_ticker_index():
    get_tick_links()
    return "Done"
@app.get("/update_ticker_funds")
async def update_ticker_funds():
    get_tick_funds()
    return "Done"
