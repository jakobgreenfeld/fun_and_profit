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


headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'Origin': 'https://www.ycombinator.com',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.ycombinator.com/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

params = {
    'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser; JS Helper (3.7.0)',
    'x-algolia-application-id': '45BWZJ1SGC',
    'x-algolia-api-key': 'Zjk5ZmFjMzg2NmQxNTA0NGM5OGNiNWY4MzQ0NDUyNTg0MDZjMzdmMWY1NTU2YzZkZGVmYjg1ZGZjMGJlYjhkN3Jlc3RyaWN0SW5kaWNlcz1ZQ0NvbXBhbnlfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiUyMnljZGNfcHVibGljJTIyJTVEJmFuYWx5dGljc1RhZ3M9JTVCJTIyeWNkYyUyMiU1RA==',
}

results = []
for i in list(string.ascii_letters):
# for i in ["a"]:
    data = '{"requests":[{"indexName":"YCCompany_production","params":"hitsPerPage=1000&maxValuesPerFacet=1000&query=&page=1&facets=%5B%22top_company%22%2C%22isHiring%22%2C%22nonprofit%22%2C%22highlight_black%22%2C%22highlight_latinx%22%2C%22highlight_women%22%2C%22batch%22%2C%22industries%22%2C%22subindustry%22%2C%22status%22%2C%22regions%22%2C%22tags%22%5D&tagFilters="}]}'

    response = requests.post('https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries', headers=headers, params=params, data=data)
    print(response.text)
    results += response.json()["results"][0]["hits"]

df = pd.DataFrame(results)
df = df.drop_duplicates(subset=['slug'])
df.to_csv('yc_scraper.csv')
# print(results)