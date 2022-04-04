import os
from dotenv import load_dotenv
load_dotenv()
PROXY = os.getenv('PROXY')
proxies = {
                "http": PROXY,
                "https": PROXY
    }
import requests
from bs4 import BeautifulSoup

import requests

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://searchmysite.net',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://searchmysite.net/search/browse/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

results = []
for pagenumber in range(1,2):
    data = 'sort=date_domain_added+desc&p=' + str(pagenumber)

    response = requests.post('https://searchmysite.net/search/browse/', data=data,headers=headers)
    print(response.text)

    print(response.status_code)
    # 

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all("a", class_="result-link")
    links = [link["href"].replace("/search/?q=","").replace("domain:","") for link in links]
    # print(len(links))
    results += links

print(results)