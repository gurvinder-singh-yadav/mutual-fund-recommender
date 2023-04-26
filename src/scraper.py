from selenium import webdriver
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup
import datetime
import time
import glob
import shutil
import os
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import json

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
    element = driver.find_elements(By.XPATH, "//div[@class='holdings101Cta cur-po']")
    if len(element) < 1:
        driver.close()
        return "element not found"
    element[0].click()
    element[0] = driver.find_element(By.XPATH, "//table[@class='tb10Table holdings101Table']")
    tbl = element[0].get_attribute("outerHTML")
    df = pd.read_html(tbl)
    df[0]["funds_name"] = pd.Series([name]*df[0].values.shape[0])
    df[0].to_csv("data/grow/{}/funds/{}.csv".format(today, name),index =None)
    print("{} is saved".format(name))
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

def get_stock_details(name) :
    root_dir = "data/stocks"
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    )
    driver.get("https://groww.in/#")
    stock_details=[]
    driver.find_element(By.XPATH,"//input[@id='globalSearch23']").send_keys(name) 
    time.sleep(1)
    driver.find_element(By.XPATH,"//input[@id='globalSearch23']").send_keys(Keys.ENTER)
    time.sleep(5)
    table = driver.find_element(By.XPATH,"(//tbody)[1]")
    trs = table.find_elements(By.TAG_NAME,"tr")
    for tr in trs:
        td = tr.find_elements(By.TAG_NAME,"td")
        for tds in td:
         stock_details.append(tds.text)
    print(stock_details)
    col = []
    results = []
    col.append('Parameter')
    results.append('results')
    for i, res in enumerate(stock_details):
        if(i%2==0):
            col.append(res)
        else:
            results.append(res)
    dict1 = dict(zip(col, results))
    path = root_dir + "/{}.json".format(name)
    
    with open(path, "w") as f:
        json.dump(dict1, f, indent=4)
    driver.close()
    return 
    

def get_stock_url(url):
    driver = webdriver.Chrome(
    ChromeDriverManager().install(),
        )
    driver.get(url)
    today = str(datetime.date.today())
    element = driver.find_elements(By.XPATH, "//div[@class='holdings101Cta cur-po']")
    if len(element) < 1:
        driver.close()
        return None
    element[0].click()
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
    if not os.path.exists("data/stocks"):
        os.mkdir("data/stocks")
    df.to_csv("data/stocks/{}.csv".format(url.split("/")[-1]), index=None)


def get_stock_urls():
    if os.path.exists("data/stocks.csv"):
        return "Already Upto Date"
    today = str(datetime.date.today())
    root_dir = "data/grow"
    path = os.path.join(root_dir, today, "index.csv")
    index = pd.read_csv(path)
    # dfs = map(get_stock_url, index["link"])
    pool = ThreadPool(os.cpu_count()*2)
    results = pool.map(get_stock_url,index["link"])

def concat_stock_urls():
    files = glob.glob("data/stocks/*.csv")
    dfs = []
    for file in files:
        dfs.append(pd.read_csv(file, index_col=None))
    df = pd.concat(dfs, ignore_index=True)
    df = df[["Name", "Link"]]
    df.to_csv("data/stocks.csv", index=None)
    shutil.rmtree("data/stocks/")
    
def get_stock_info(stock):
        idx, (name, url) = stock
        driver = webdriver.Chrome(
        ChromeDriverManager().install(),
                )
        driver.get(url)
        stock = {}
        try:
            element = driver.find_element(By.XPATH, "//body[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[4]/div[1]/section[1]/section[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]")
            stock["todaymin"] = element.get_attribute("aria-valuemin")
            stock["todaymax"] =  element.get_attribute("aria-valuemax")
            stock["todaynow"] = element.get_attribute("aria-valuenow")
            element = driver.find_element(By.XPATH, "//body[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[4]/div[1]/section[1]/section[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]")
            stock["52min"] = element.get_attribute("aria-valuemin")
            stock["52max"] =  element.get_attribute("aria-valuemax")
            stock["52now"] = element.get_attribute("aria-valuenow")
            xpath = "//body/div[@id='__next']/div[@id='root']/div/div[contains(@class,'container web-align')]/div[@class='row pw14Container']/div[@class='pw14MainWrapper']/div[@class='pw14ContentWrapper']/div[@class='col l12']/div[@class='container web-align']/div[@class='col l12 stkP12BelowFoldDiv']/div[@class='col l12 stkP12BelowFoldInnerCont']/div[@class='col l12']/div[@class='col l12']/div[@class='col l12']/section/section/div[@class='onMount-appear-done onMount-enter-done']/div[1]"
            div = driver.find_element(By.XPATH, xpath)
            innerhtml = div.get_attribute("innerHTML")
            soup = BeautifulSoup(innerhtml, "html.parser")
            names = [i.text for i in soup.find_all("div", {"class" : "stpp34KeyText stpp34KeyTextStk fs14"})]
            values = [i.text for i in soup.find_all("span", {"class": "stpp34Value fs16"})]
            element = driver.find_element(By.XPATH, "//table[@class='tb10Table col l12 ft785Table']")
            trs = element.find_elements(By.TAG_NAME, "tr")
            for i in range(len(trs)):
                    tds = trs[i].find_elements(By.TAG_NAME, "td")
                    names.append(tds[0].text)
                    values.append(tds[1].text)
            xpath =  "//div[@class='col l12 stkP12Section onMount-appear-done onMount-enter-done']//table[1]"
            element = driver.find_element(By.XPATH, xpath)
            trs = element.find_elements(By.TAG_NAME, "tr")
            for i in range(len(trs)):
                    tds = trs[i].find_elements(By.TAG_NAME, "td")
                    names.append(tds[0].text)
                    values.append(tds[1].text)
            xpath = "//div[@class='col l12 stkP12Section onMount-appear-done onMount-enter-done']//table[2]"
            element = driver.find_element(By.XPATH, xpath)
            trs = element.find_elements(By.TAG_NAME, "tr")
            for i in range(len(trs)):
                    tds = trs[i].find_elements(By.TAG_NAME, "td")
                    names.append(tds[0].text)
                    values.append(tds[1].text)
            stock.update(dict(zip(names, values)))
            driver.close()
            root_dir = "data/stock"
            path = os.path.join(root_dir, "{}.json".format(idx))
            result = {"name" : name, 
                    "info" : stock
                            }
            # print(path)
            with open(path, 'w') as f:
                json.dump(result, f, indent=4)
            return "Done"
        except:
            pass
        
def get_stocks_info():
    df = pd.read_csv("data/stocks.csv")
    root_dir = "data/stock"
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    if len(os.listdir(root_dir)) > 1:
        return "Already updated"
    pool = ThreadPool(os.cpu_count()*2)
    pool.map(get_stock_info,enumerate(df.values))

def summarise_stocks():
    files = glob.glob("data/stock/*.json")
    data = {}
    data["name"] = []
    with open(files[0], "r") as f:
        js = json.load(f)
        keys = js["info"].keys()
        for key in keys:
            if key  == "NSE Symbol" or key == "BSE Symbol":
                data["Symbol"] = []
            else:
                data[key] = []
    for file in files:
            with open(file, "r") as f:
                js = json.load(f)
                data["name"].append(js["name"])
                for key in js["info"].keys():
                    if key  == "NSE Symbol" or key == "BSE Symbol":
                        data["Symbol"].append(js["info"].get(key, None))
                    else:
                        data[key].append(js["info"].get(key, None))
    # for k, v in data.items():
    #     print(k, len(v))
    df = pd.DataFrame(data)
    df.to_csv("data/stock_info.csv", index=None)
        
    
    
