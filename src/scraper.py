from selenium import webdriver
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
import datetime
import time
import os
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def get_page_summary(page):
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    )
    base_url = "https://groww.in/mutual-funds/filter?q=&fundSize=&category=%5B%22Equity%22%5D&pageNo={}&sortBy=3".format(page)
    driver.get(base_url)
    table = driver.find_element(By.CLASS_NAME, "tb10Table")
    elements = table.find_elements(By.TAG_NAME, "tr")
    data = {
        "name":[],
        "link":[],
        "risk":[]
    }
    for element in elements:
        link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
        td = element.find_elements(By.TAG_NAME, "td")
        fund = td[1].text.split("\n")
        data['link'].append(link)
        data["name"].append(fund[0])
        data["risk"].append(fund[1])
    driver.close()
    return pd.DataFrame(data)

def save_summaries(pages = 28):
    date = str(datetime.date.today())
    root_dir = "data/grow"
    index_path = os.path.join(root_dir, date, "index", "index.csv")
    if os.path.exists(index_path):
        return "no need to scrape"
    if not os.path.exists(os.path.join(root_dir, date, "index")):
        os.makedirs(os.path.join(root_dir, date, "index"))
        for page in tqdm(range(pages)):
            data = get_page_summary(page)
            path = os.path.join(root_dir, date, "index", "{}.csv".format(page))
            data.to_csv(path, index=None)
    return "scraped"
def concat(dir, file_name = "index.csv"):
    paths = os.listdir(dir)
    dfs = []
    # print(paths)
    if len(paths) > 1:
        for path in paths:
            path = os.path.join(dir, path)
            dfs.append(pd.read_csv(path, index_col=None))
            os.remove(path)
        df = pd.concat(dfs)
        df.to_csv(os.path.join(dir, file_name), index=None)

def scrape_fund(name,url):
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
        )
    driver.get(url)
    element = driver.find_element(By.XPATH, "//div[@class='holdings101Cta cur-po']")
    element.click()
    element = driver.find_element(By.XPATH, "//table[@class='tb10Table holdings101Table']")
    tbl = element.get_attribute("outerHTML")
    df = pd.read_html(tbl)
    df[0].to_csv("data/grow/2023-04-23/funds/{}.csv".format(name),index =None)
    driver.close()
def scrape_funds():
    date = str(datetime.date.today())
    funds_dir = os.path.join("data/grow",date, "funds")
    index_dir = os.path.join("data/grow",date, "index")
    index_path = os.path.join(index_dir, os.listdir(index_dir)[0])
    if os.path.exists(funds_dir):
        return "already up to date"
    else:
        os.mkdir(funds_dir)
        index = pd.read_csv(index_path)[["name", "link"]].values()
        pool = ThreadPool(os.cpu_count())
        pool.starmap(scrape_fund, index)
        return "Updated"
