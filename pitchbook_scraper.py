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

import string
import multiprocessing
import pandas as pd
import sitemap_scraper

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    r = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def scrape_pitchbook_profile(url):
    details = {}
    details["url"] = url

    try:
        soup = get_soup(url)
        details['name'] = soup.find('h2').text.replace("Overview","").strip()
        details["description"] = soup.find("div",class_="pp-description").find("p").text.strip()
    except:
        pass
    return details

def scrape_all_profiles():
    df = pd.read_csv("pitchbook_profiles.csv")
    urls = df["url"].tolist()

    with multiprocessing.Pool(processes=12) as pool:
        results = pool.map(scrape_pitchbook_profile, urls[:4])
    
    dff = pd.DataFrame(results)
    dff.to_csv("pitchbook_profiles_details.csv", index=False)


### METHOD 1: BRUTE FORCE SEARCH

def scrape_search_results(keyword):
    url = "https://pitchbook.com/profiles/search?q=" + keyword
    soup = get_soup(url)
    result_container = soup.find("ul",class_="profile-list")
    results = []
    for li in result_container.find_all("li"):
        profile_url = "https://pitchbook.com" + li.find("a")["href"]
        results.append(profile_url)
    return results

def prepare_keywords():
    # keywords = []
    keywords1 = list(string.ascii_lowercase)
    # product of combinations of 2 letters
    keywords2 = [a+b for a in keywords1 for b in keywords1]
    # product of combinations of 3 letters
    # keywords3 = [a+b+c for a in keywords1 for b in keywords1 for c in keywords1]
    keywords = keywords2  + keywords1
    return keywords

def scrape_all_search_results():
    keywords = prepare_keywords()
    
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(scrape_search_results, keywords[:4])
    
    results = [item for sublist in results for item in sublist]
    print(len(results))
    results = list(set(results))
    print(len(results))
    return results



### METHOD 2: USING A SEARCH ENGINE

def scrape_duckduckgo(keyword):
    url = "https://duckduckgo.com/html/?q=" + keyword
    try:
        soup = get_soup(url)
        links = soup.find_all("a",class_="result__snippet")
        links = [link["href"] for link in links]
    except:
        links = []
    return links

def scrape_all_duckduckgo_results():
    keywords = prepare_keywords()
    keywords = ["site:pitchbook.com/profiles " + keyword for keyword in keywords]
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(scrape_duckduckgo, keywords[:4])
    
    results = [item for sublist in results for item in sublist]
    print(len(results))
    results = [x.rstrip("/") for x in results if "pitchbook.com/profiles" in x]
    results = list(set(results))
    print(len(results))
    
    return results

## METHOD 3: SITEMAP SCRAPING

def get_all_public_profiles_urls():
    # get all the urls from the sitemap
    urls = sitemap_scraper.scrape_sitemap("https://pitchbook.com/sitemap.xml")
    # get all the urls from the gz files
    public_profiles_urls = []
    for url in urls[:5]:
        if 'public-profiles' in url:
            public_profiles_urls += sitemap_scraper.download_and_extract_gz_file(url)
    # return the list of public profiles urls
    return public_profiles_urls


if __name__ == "__main__":
    # print(scrape_duckduckgo("site:pitchbook.com/profiles"))
    # print(prepare_keywords())
    res = get_all_public_profiles_urls()
    df = pd.DataFrame(res,columns=["url"])
    df.to_csv("pitchbook_profiles.csv", index=False)