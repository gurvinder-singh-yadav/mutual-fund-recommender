from selenium import webdriver
from tqdm import tqdm


from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument("--headless")

class Grow:
    def __init__(self) -> None:
        self.get_driver()
        self.baseIndex = "https://groww.in/mutual-funds/filter?q=&fundSize=&category=%5B%22Equity%22%5D&pageNo={}&sortBy=3"
        self.path = ""
    def get_driver(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver", options=chromeOptions)
    def visit(self, url = ""):
        self.driver.get(url)
    def close_driver(self):
        self.driver.close()
    def funds_url(self, n = 1):
        self.fundsUrl = []
        for i in tqdm(range(6,n)):
            try:
                self.visit(self.baseIndex.format(i))
                table = self.driver.find_element_by_class_name("tb10Table")
                aTags = table.find_elements_by_tag_name("a")
                for a in aTags:
                    link = a.get_attribute('href')
                    self.fundsUrl.append(link)
            except:
                break
    def get_fund_distribution(self):
        self.funds = {}
        index = 0
        for fund in tqdm(self.fundsUrl):
            self.driver.get(fund)
            try: 
                div = self.driver.find_element_by_class_name("holdings101TableContainer")
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
            
            self.funds[fund.split("/")[-1]] = table
            index += 1
            if((index % 10 == 0) and (index != 0)):
                self.close_driver()
                self.get_driver()




        