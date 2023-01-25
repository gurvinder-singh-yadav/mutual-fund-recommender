from src.scraper import get_grow
from fastapi import FastAPI
import time



app = FastAPI()

@app.get("/")
def read_root():
        return "Hello World!"

@app.get("/update_grow_dataset")
def data_downloader():
        print("Updating")
        start = time.time()
        get_grow()      
        time_taken = time.time() - start
        return "Updated the dataset in " + str(time_taken)


