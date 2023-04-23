from src.scraper import save_summaries, concat, scrape_funds
import os
import pandas as pd
import datetime
from fastapi import FastAPI

app = FastAPI()

@app.get("/update_index")
async def update_index():
    save_summaries()
    today = str(datetime.date.today())
    concat("data/grow/{}/index".format(today))
    return "Updated"

@app.get("/")
async def root():
    return "you are in page"

@app.get("/update_funds")
async def update_funds():
    scrape_funds()
    return "Done"