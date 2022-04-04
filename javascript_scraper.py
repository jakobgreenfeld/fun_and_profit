import os
from dotenv import load_dotenv
load_dotenv()
PROXY = os.getenv('PROXY')
proxies = {
                "http": PROXY,
                "https": PROXY
    }
import requests
import pandas as pd 
import string
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def scrape(url):
    # session = HTMLSession()
    # response = session.get(url, proxies=proxies)
    # response.html.render()
    response = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")
    res = soup.find_all("td")
    # render
    
    print(len(res))
    return soup

if __name__ == "__main__":
    url = "https://coinmarketcap.com/"
    data = scrape(url)
    # print(data)

