import os
from dotenv import load_dotenv
load_dotenv()
PROXY = os.getenv('PROXY')
proxies = {
                "http": PROXY,
                "https": PROXY
    }
RALLY_USERNAME = os.getenv('RALLY_USERNAME')
RALLY_PASSWORD = os.getenv('RALLY_PASSWORD')
import requests
import pandas as pd 
import string
from bs4 import BeautifulSoup
import re
import cloudscraper
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--disable-gpu')
userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
chrome_options.add_argument(f'user-agent={userAgent}')

def scrape_javascript(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)

    el = driver.find_element_by_class_name("menu-item-143").click()
    time.sleep(2)

    email_field = driver.find_element_by_name("email").send_keys(RALLY_USERNAME)
    password_field = driver.find_element_by_name("password").send_keys(RALLY_PASSWORD)
    time.sleep(2)
    login_button = driver.find_element_by_class_name("AuthenticationPages-actionButton").click()
    time.sleep(20)

    assets = driver.find_elements_by_class_name("AssetItem-info-name")
    print(len(assets))
    results = []
    for asset in assets:
        print(asset.text)
        results.append(asset.text)

    
    driver.close()
    driver.quit()
    return results



def scrape_assets():
    url = "https://api.production.rallyrd.com/api/v2/assets/"
    r = requests.get(url, proxies=proxies)
    rson = r.json()
    print(rson)
    return rson["items"]

def get_rally_json_data():

    for i in range(0,10):
        try:
            url = "https://api.production.rallyrd.com/api/v3/auth/login/"
            # url = "https://rallyrd.com"
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:71.0) Gecko/20100101 Firefox/71.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
            payload = {"email":RALLY_USERNAME,"password":RALLY_PASSWORD,"remember_me":True}
            scraper = cloudscraper.create_scraper()
            # session = requests.Session()
            raw = scraper.post(url,json=payload, headers=headers)
            rawson = raw.json()
            jwttoken = rawson["token"]
            
            headers = {"Authorization": "JWT " + jwttoken,"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:71.0) Gecko/20100101 Firefox/71.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
            # print(headers)
            r = scraper.get("https://api.production.rallyrd.com/api/v2/assets/", headers=headers)
            # print(r.text)
            rson = r.json()
            # print(rson)
            break
        except:
            pass
    return rson["items"]

if __name__ =="__main__":
    # res = get_rally_json_data()
    # df = pd.DataFrame(res)
    # df.to_csv("rally_data.csv", index=False)
    # r = get_rally_json_data()
    # print(r)
    scrape_javascript("https://rallyrd.com")