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

def scrape_bestsellers(root_url):
    url = root_url + "/collections/best-sellers/products.json?limit=250"
    response = requests.get(url, proxies=proxies)
    data = response.json()
    return data["products"]

if __name__ == "__main__":
    root_url = "https://articture.com"
    data = scrape_bestsellers(root_url)
    df = pd.DataFrame(data)
    df.to_csv("articture_bestsellers.csv",index=False)
