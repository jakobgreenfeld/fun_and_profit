import requests

url = "https://angellist.com"
r = requests.get(url)

#### HEADERS

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
}
r = requests.get(url, headers=HEADER)

#### PROXIES

WEBSHARE_USERNAME = 'sdfbfasjnd-rotate'
WEBSHARE_PASSWORD = 'jndandnaskfndasd'
PROXY = "http://{}:{}@p.webshare.io:80/".format(WEBSHARE_USERNAME, WEBSHARE_PASSWORD)
proxies = {
                "http": PROXY,
                "https": PROXY
    }

for i in range(10):
    r = requests.get(url, proxies=proxies)
    if r.status_code == 200:
        print("Success")
        break
r = requests.get(url, proxies=proxies,headers=HEADER)

#### SCRAPER API

SCRAPER_API_KEY = "kkfnasjkdnkajsnkdnask"
r =  requests.get('http://api.scraperapi.com?api_key={}&url={}'.format(SCRAPER_API_KEY, url))

#### SCRAPING BEE

BEE_API_KEY = "ffnajksdbnjasfbasmngagnaksjkdnansjn"
r =  requests.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': BEE_API_KEY,
            'url': url, 
            "block_resources":'false',
            'premium_proxy': 'false', 
            'country_code':'us',
            'render_js': 'false',
        }, 
    )

#### REQUESTS HTML 
#### pip install requests-html

from requests_html import HTMLSession
session = HTMLSession()
r = session.get(url)
r.html.render()
print(r.html.html)

# session = requests.Session()
# r = session.get(url)

