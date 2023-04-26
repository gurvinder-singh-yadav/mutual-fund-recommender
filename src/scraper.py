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
    ChromeDriverManager().install(),
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
    date = str(datetime.date.today())
    root_dir = "data/grow"
    path = os.path.join(root_dir, date, "index", "{}.csv".format(page))
    data = pd.DataFrame(data)
    data.to_csv(path, index=None)

def save_summaries(pages = 28):
    date = str(datetime.date.today())
    root_dir = "data/grow"
    index_path = os.path.join(root_dir, date, "index.csv")
    if os.path.exists(index_path):
        return "no need to scrape"
    if not os.path.exists(os.path.join(root_dir, date, "index")):
        os.makedirs(os.path.join(root_dir, date, "index"))
        pool = ThreadPool(os.cpu_count())
        pool.map(get_page_summary, range(28))
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
    ChromeDriverManager().install(),
        )
    today = str(datetime.date.today())
    driver.get(url)
    date = str(datetime.date.today())
    element = driver.find_element(By.XPATH, "//div[@class='holdings101Cta cur-po']")
    element.click()
    try:
        element = driver.find_element(By.XPATH, "//table[@class='tb10Table holdings101Table']")
        tbl = element.get_attribute("outerHTML")
        df = pd.read_html(tbl)
        df[0].to_csv("data/grow/{}/funds/{}.csv".format(today, name),index =None)
    except:
        print("Page Not Found")
    driver.close()
def scrape_funds():
    date = str(datetime.date.today())
    if os.path.exists(os.path.join("data/grow",date, "funds.csv")):
        return "Data Upto Date"
    funds_dir = os.path.join("data/grow",date, "funds")
    index_path = os.path.join("data/grow",date, "index.csv")
    if os.path.exists(funds_dir):
        return "already up to date"
    else:
        os.mkdir(funds_dir)
        index = pd.read_csv(index_path)[["name", "link"]].values
        pool = ThreadPool(os.cpu_count())
        pool.starmap(scrape_fund, index)
        return "Updated"

def get_stock_url(url):
    driver = webdriver.Chrome(
    ChromeDriverManager().install(),
        )
    driver.get(url)
    element = driver.find_element(By.XPATH, "//div[@class='holdings101Cta cur-po']")
    element.click()
    try: 
        table = driver.find_element(By.XPATH, "//table[@class='tb10Table holdings101Table']")
        trs = table.find_elements(By.TAG_NAME, 'tr')
        stock_names = []
        stock_url = []
        for i in range(1, len(trs)):
            try:
                name = trs[i].find_element(By.TAG_NAME, "td").text
                link = trs[i].find_element(By.TAG_NAME, "a").get_attribute("href")
                stock_names.append(name)
                stock_url.append(link)
            except:
                continue
        driver.close()
        df = pd.DataFrame({"Name":stock_names,
                        "Link": stock_url
                        })
        return df
    except:
        return None




def get_tick_links():
    date = str(datetime.date.today())
    root_dir = "data/tick"
    index_path = os.path.join(root_dir, date, "indext", "indext.csv")
    if not os.path.exists(os.path.join(root_dir, date, "indext")):
        os.makedirs(os.path.join(root_dir, date, "indext"))
        driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        )
        driver.get("https://ticker.finology.in/investor")
        fundsUrl = []
        table = driver.find_element(By.XPATH,"/html/body/form/div[5]/div[2]")
        aTags = table.find_elements(By.TAG_NAME, "a")
        for a in aTags:
                    link = a.get_attribute('href')
                    fundsUrl.append(link)    
        dict1 = {"url":(fundsUrl)}
        df = pd.DataFrame(dict1)
        df.to_csv(index_path, index=None)
        driver.close()



def get_tick_funds():
  root_dir = "data/tick"
  date = str(datetime.date.today())
  funds_path=os.path.join(root_dir, date, "fundst")
  index_path = os.path.join(root_dir, date,"indext", "indext.csv" )
  if not os.path.exists(funds_path):
     os.makedirs(os.path.join(root_dir, date, "fundst"))

     df = pd.read_csv(index_path)
     fundsUrl = df.values.reshape(-1)
     driver = webdriver.Chrome(
     ChromeDriverManager().install(),
        )
     for i in range(0,70):
                table=[]
                print(fundsUrl[i])
                driver.get(fundsUrl[i])
                rows= driver.find_element(By.TAG_NAME,"tbody")
                tr_tags =rows.find_elements(By.TAG_NAME,"tr")
                for tr in tr_tags:
                   cols=[]
                   td_tags=tr.find_elements(By.TAG_NAME,'td')
                   driver.execute_script("arguments[0].scrollIntoView()",tr)

                   for col in td_tags:
                       cols.append(col.text)  
                   table.append(cols)
                file_name = fundsUrl[i].split("/")[-1]
                df = pd.DataFrame(table)
                date = str(datetime.date.today())
                df.to_csv(funds_path + "/{}.csv".format(file_name), index=None)
            
    