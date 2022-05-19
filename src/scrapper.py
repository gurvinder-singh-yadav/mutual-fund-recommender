import requests
from bs4 import BeautifulSoup
def scrape(k = 0):
    base = "https://groww.in"
    fundnames_url = "https://groww.in/mutual-funds/filter?q=&fundSize=&categories=%7B%22Debt%22%3Afalse%2C%22Equity%22%3A%7B%22type%22%3A%22category%22%2C%22value%22%3A%22Equity%22%2C%22subCategories%22%3A%5B%5D%7D%7D&pageNo={}&sortBy=0".format(k)
    page = requests.get(fundnames_url)
    soup = BeautifulSoup(page.content,"html.parser")
    x = soup.find_all("a","pos-rel f22Link")
    data = {}
    for i in range(len(x)):
        x[i]["href"]
        str(x[i]["href"]).split("/")[-1]
        info_page = base + str(x[0]["href"])
        info_page_1 = requests.get(info_page)
        page_1 = BeautifulSoup(info_page_1.content,"html.parser")
        temp = page_1.find_all("tr","holdings101Row")
        l2 = []
        for j in range(len(temp)):
            temp1 = temp[j].find_all("td")
            l1 = []
            for k in range(len(temp1)):
                l1.append(temp1[k].text) 
            l2.append(l1)
        data[str(x[i]["href"]).split("/")[-1]] = l2
    return data