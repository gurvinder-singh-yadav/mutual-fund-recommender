from selenium import webdriver
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
import time
import json
import pandas as pd

from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument("--headless")

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]
class Grow:
    def __init__(self):
        self.baseIndex = "https://groww.in/mutual-funds/filter?q=&fundSize=&category=%5B%22Equity%22%5D&pageNo={}&sortBy=3"
        self.path = "data/grow/"
        self.processes = 8
        self.pool = ThreadPool(processes=self.processes)
        self.get_driver()
    def get_driver(self):
        self.drivers = [webdriver.Chrome(executable_path="./chromedriver", options=chromeOptions) for i in range(self.processes)]
    def visit(self, driver_index,url = ""):
        self.drivers[driver_index].get(url)
    def close_driver(self, driver_index):
        self.drivers[driver_index].close()
    def funds_url(self,driver_index ,n = 1):
        self.fundsUrl = []
        for i in tqdm(range(0,n)):
            try:
                self.visit(0,self.baseIndex.format(i))
                table = self.drivers[driver_index].find_element_by_class_name("tb10Table")
                aTags = table.find_elements_by_tag_name("a")
                for a in aTags:
                    link = a.get_attribute('href')
                    self.fundsUrl.append(link)
            except:
                break
    def get_funds_table(self):
        def worker(funds, driver_index):
            for fund in tqdm(funds):
                self.drivers[driver_index].get(fund)
                try: 
                    div = self.drivers[driver_index].find_element_by_class_name("holdings101TableContainer")
                except:
                    continue
                divN = div.find_element_by_xpath("//div[contains(@class, 'holdings101Cta cur-po') and text()='See All']")
                divN.click()
                try:
                    rows = div.find_elements_by_class_name('holdings101Row')
                except:
                    continue
                table = []
                for row in rows:
                    cols = []
                    td = row.find_elements_by_tag_name('td')
                    for col in td:
                        cols.append(col.text)
                    table.append(cols)
                file_name = fund.split("/")[-1]
                df = pd.DataFrame(table)
                df.columns = ["Name","Sector","Instrument","Assets"]
                # print("data/grow/" + file_name + ".csv")
                df.to_csv(self.path + file_name +".csv", index=None)
            return 1
        total_funds = len(self.fundsUrl)

        x = list(divide_chunks(self.fundsUrl, total_funds // self.processes))
        x_len = len(x)
        results = []
        processes = list(range(x_len))
        print("Assigning work to different workers")
        for i in tqdm(range(x_len)):
            results.append(self.pool.apply_async(worker, args=(x[i], processes[i])))
        print("Computing Assigned work by differnt workers Asynchronously")
        
        # for i in (range(x_len)):
        #     results[i] = results[i].get()
        return (x_len, len(results))
    def close_pool(self):
        self.pool.close()

def get_grow(dir = '/', pages=28):
    obj = Grow()
    obj.funds_url(0,28)
    results = obj.get_funds_table()
    # print(results)
    obj.close_pool()