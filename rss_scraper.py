import feedparser # pip install feedparser
from urllib.request import ProxyHandler, build_opener
import pandas as pd
from bs4 import BeautifulSoup



import os
from dotenv import load_dotenv
load_dotenv()
PROXY = os.getenv('PROXY')
proxies = {
                "http": PROXY,
                "https": PROXY
    }

proxy_handler = ProxyHandler(proxies)

def parse_feed(url):
    d = feedparser.parse(url, handlers=[proxy_handler])

    results = []
    for e in d.entries:
        details = {}
        try:
            details["title"] = e.title
        except:
            pass
        try:
            details["published"] = e.published
        except:
            pass
        try:
            details["link"] = e.link
        except:
            pass
        try:
            # description = BeautifulSoup(e.description, "html.parser").get_text(" ")
            details["content"] = e.content
        except:
            pass
        results.append(details)
    return results 

def scrape_news(keyword):
    url = "https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en".format(keyword)
    return parse_feed(url)

def scrape_jobs(keyword):
    url = "https://rss.indeed.com/rss?q={}".format(keyword)
    return parse_feed(url)

def scrape_freelance_jobs(keyword):
    url = "https://www.upwork.com/ab/feed/jobs/rss?q={}".format(keyword)
    return parse_feed(url)

if __name__ == "__main__":
    # data = scrape_news("nike")
    # df = pd.DataFrame(data)
    # df.to_csv("news.csv",index=False)

    # data = scrape_jobs("nike")
    # df = pd.DataFrame(data)
    # df.to_csv("jobs.csv",index=False)

    data = scrape_freelance_jobs("scraping")
    df = pd.DataFrame(data)
    df.to_csv("scraping_jobs.csv",index=False)