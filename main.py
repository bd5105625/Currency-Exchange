# get exchange rate from website

# from collections.abc import Mapping
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import re
import pandas as pd

urls = ["https://www.esunbank.com.tw/bank/personal/deposit/rate/forex/foreign-exchange-rates",
            'https://www.wellsfargo.com/foreign-exchange/currency-rates/',
            'https://www.mufg.co.id/charges/today-exchange-rates',
            'https://www.bankofengland.co.uk/boeapps/database/Rates.asp?Travel=NIxAZx&into=GBP',
            'https://bank.shinhan.com/index.jsp#020501010000',
            'https://www.bangkokbank.com/en/Personal/Other-Services/View-Rates/Foreign-Exchange-Rates']

class Calculator:

    def __init__(self) -> None:
        self.currency = ['TWD', 'USD', 'JPY', 'GBP', 'THB', 'KRW']
        self.nation = ["TAIWAN", "UNITED STATES", "JAPAN", "GREAT BRITAIN", "THAILAND", "SOUTH KOREA"]
        self.urls = ["https://www.esunbank.com.tw/bank/personal/deposit/rate/forex/foreign-exchange-rates"]
        self.twd_rate = {}
        self.usd_rate = {}
        self.jpy_rate = {}
        self.gbp_rate = {} #england pound
        self.thb_rate = {} #thailand bath
        self.krw_rate = {} #korea won
        self.driver = webdriver.Edge('./msedgedriver.exe')
        self.get_data()


    def get_taiwan(self):
        print("get taiwan exchange rate")
        url = "https://www.esunbank.com.tw/bank/personal/deposit/rate/forex/foreign-exchange-rates"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        # beautiful find specific tag and id
        content = soup.find('div', id='exchangeRate')
        # find using class name
        table = content.find('tbody', class_='l-exchangeRate__table result')
        # find all
        table2 = table.find_all('tr')
        for item in table2:
            # print(item)
            # print("ALL", item.find('div', class_='col-auto px-3 col-lg-5 title-item'))
            name = item.find_all('div', class_="col-1 col-lg-2 title-item title-en")
            if name:
                # remove any character except alphabet
                curr_name = re.sub(r'[^a-zA-Z]', '', name[0].text)
                # print("curr_name", curr_name)
                # curr_name = name[0].text.replace(" ", "")
                exchange_rate = item.find_all('div', class_='SBoardRate')
                if curr_name in self.currency:
                    self.twd_rate[curr_name] = float(exchange_rate[0].text)
                # exchange = item.find_all('div', class_='BBoardRate')
                # print("BANK BUY", exchange)
                # exchange = item.find_all('div', class_='SBoardRate')
                # print("BANK SELL", exchange[0].text)


        url = 'https://rate.bot.com.tw/xrt/flcsv/0/day'   
        rate = requests.get(url)   
        rate.encoding = 'utf-8'  
        rt = rate.text            
        rts = rt.split('\n')      
        for i in rts:              
            try:                             
                a = i.split(',')             
                if a[0] == 'KRW':
                    self.twd_rate['KRW'] = a[12]
                    # self.twd_rate[a[0]] = a[12]
            except:
                break
        print("twd_rate", self.twd_rate)

    def get_usd(self):
        print("get united states exchange rate")
        default_url = "https://www.wellsfargo.com/foreign-exchange/currency-rates/"
        curr_name = ["TAIWAN", "JAPAN", "GREAT", "THAILAND", "SOUTH"]
        self.driver.get(default_url)
        self.driver.current_url
        button = self.driver.find_element(By.ID, 'tab-allcurrencies')
        button.click()
        contents = self.driver.find_element(By.ID, "allcurrencies").text.split('\n')
        contents = contents[58:]
        for content in contents:
            items = content.split(' ')
            # print(items)
            if items[0] in curr_name:
                if items[0] == "TAIWAN":
                    self.usd_rate['TWD'] = float(items[-2])
                elif items[0] == "JAPAN":
                    self.usd_rate['JPY'] = float(items[-2])
                elif items[0] == "GREAT":
                    self.usd_rate['GBP'] = float(items[-2])
                elif items[0] == "THAILAND":
                    self.usd_rate['THB'] = float(items[-2])
                elif items[0] == "SOUTH" and items[1] == "KOREA":
                    self.usd_rate['KRW'] = float(items[-2])
        print("usd_rate", self.usd_rate)

    
    def get_jpy(self):
        print("get japan exchange rate")
        curr_name = [""]
        default_url = "https://www.tokyo-card.co.jp/wcs/en/rate.php"
        self.driver.get(default_url)
        self.driver.current_url
        contents = self.driver.find_elements(By.CLASS_NAME, "block")[1].text.split('\n')
        for content in contents:
            items = content.split(' ')
            if len(items) >= 3 and items[-3] in self.currency:
                self.jpy_rate[items[-3]] = float(items[-2])
        print("jpy_rate", self.jpy_rate)
    
    def get_gbp(self):
        print("get england exchange rate")
        curr_name = ['Taiwan', 'US', 'Japanese', 'British', 'Thai', 'South']
        default_url = "https://www.bankofengland.co.uk/boeapps/database/Rates.asp?Travel=NIxAZx&into=GBP"
        self.driver.get(default_url)
        self.driver.current_url
        contents = self.driver.find_element(By.CLASS_NAME, "table").text.split('\n')
        for content in contents:
            items = content.split(' ')
            if items[0] in curr_name:
                if items[1] == 'African':
                    continue
                if items[0] == 'Taiwan':
                    self.gbp_rate['TWD'] = float(items[-3])
                elif items[0] == 'US':
                    self.gbp_rate['USD'] = float(items[-3])
                elif items[0] == 'Japanese':
                    self.gbp_rate['JPY'] = float(items[-3])
                elif items[0] == 'British':
                    self.gbp_rate['GBP'] = float(items[-3])
                elif items[0] == 'Thai':
                    self.gbp_rate['THB'] = float(items[-3])
                elif items[0] == 'South':
                    self.gbp_rate['KRW'] = float(items[-3])
        print("gbp_rate", self.gbp_rate)

    
    def get_thb(self):
        print("get thailand exchange rate")
        default_url = 'https://www.bangkokbank.com/en/Personal/Other-Services/View-Rates/Foreign-Exchange-Rates'
        self.driver.get(default_url)
        self.driver.current_url
        contents = self.driver.find_element(By.CLASS_NAME, "table-outer").text.split('\n')
        for content in contents:
            items = content.split(' ')
            if items[0] in self.currency:
                self.thb_rate[items[0]] = float(items[-4])
            if items[0] == 'USD50':
                self.thb_rate['USD'] = float(items[-4])
        print("thb_rate", self.thb_rate)
    
    def get_krw(self):
        print("get korea exchange rate")
        default_url = 'https://omoney.kbstar.com/quics?page=C021159#loading'
        self.driver.get(default_url)
        self.driver.current_url
        contents = self.driver.find_element(By.CLASS_NAME, "btnTable").text.split('\n')
        for content in contents:
            items = content.split(' ')
            # print(items[0].split())
            if items[0].split('(')[0] in self.currency:
                self.krw_rate[items[0].split('(')[0]] = float(items[-8].replace(',', ''))
        print("krw_rate", self.krw_rate)

        
    def get_data(self):
        self.get_taiwan()
        self.get_usd()
        self.get_jpy()
        self.get_gbp()
        self.get_thb()
        self.get_krw()


def __init__():
    # print("here")
    # one input
    print("What do you want to do?\n")
    print("Option A: Exchange to specific currency")
    print("Option B: Get maximum value of exchange")
    option = input()
    if option == 'A':
        print("Please input the currency you want to exchange")
        currency = input()
        print("Please input the amount of money you want to exchange")
        amount = input()
        print("Please input the currency you want to exchange to")
        exchange = input()
    else:
        print("B")

    res = Calculator()
    
    return 0

if __name__ == "__main__":
    __init__()