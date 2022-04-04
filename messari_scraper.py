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


def get_messari_assets_algolia():
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
        'x-algolia-application-id': '3B439ZGYM3',
        'x-algolia-api-key': '14a0c8d17665d52e61167cc1b2ae9ff1',
    }

    results = []
    for i in list(string.ascii_letters)[:3]:
    # for i in ["a"]:
        data = '{"requests":[{"indexName":"entity","params":"hitsPerPage=1000&maxValuesPerFacet=1000&query='+i +'&page=0&facets=%5B%22top_company%22%2C%22isHiring%22%2C%22nonprofit%22%2C%22highlight_black%22%2C%22highlight_latinx%22%2C%22highlight_women%22%2C%22batch%22%2C%22industries%22%2C%22subindustry%22%2C%22status%22%2C%22regions%22%2C%22tags%22%5D&tagFilters="}]}'
        # data = '{"requests":[{"indexName":"entity","params":"hitsPerPage=1000&highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&query=a&filters=NOT%20type%3Achart&facets=%5B%5D&tagFilters="}]}'

        response = requests.post('https://3b439zgym3-dsn.algolia.net/1/indexes/*/queries', headers=headers, params=params, data=data)
        print(response.text)
        results += response.json()["results"][0]["hits"]

    df = pd.DataFrame(results)
    df = df.drop_duplicates(subset=['slug'])
    df.to_csv('messari_scraper.csv')
    

def get_messari_asset_details_graphql(slug):

    headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'accept': '*/*',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'sec-ch-ua-platform': '"macOS"',
    'Origin': 'https://messari.io',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://messari.io/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    json_data = {
        'operationName': 'AssetForHeader',
        'variables': {
            'slug': slug,
        },
        'query': 'query AssetForHeader($slug: String!) {\n  assetBySlug(slug: $slug) {\n    id\n    name\n    slug\n    symbol\n    general {\n      id\n      isVerified\n      isResearchHub\n      links {\n        link\n        name\n        type\n        __typename\n      }\n      platformContracts {\n        platform\n        contractAddress\n        __typename\n      }\n      sector\n      tagline\n      __typename\n    }\n    tokenEconomics {\n      id\n      tokenUsage {\n        tokenType\n        __typename\n      }\n      __typename\n    }\n    metrics {\n      id\n      pricing {\n        id\n        price\n        __typename\n      }\n      returnOnInvestment {\n        id\n        change24Hour: change(span: ONE_DAY)\n        __typename\n      }\n      ranks {\n        id\n        absoluteRank\n        sectorRanks: relativeRank(comparison: RELATIVE_BY_SECTOR) {\n          among\n          rank\n          __typename\n        }\n        tagRanks: relativeRank(comparison: RELATIVE_BY_TAG) {\n          among\n          rank\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
    }

    response = requests.post('https://graphql.messari.io/query', headers=headers, json=json_data)
    # print(response.text)
    results = response.json()["data"]["assetBySlug"]

    results["price"] = results["metrics"]["pricing"]["price"]

    try:
        keys = results["general"].keys()
        for k in keys:
            results[k]= results["general"][k]
        del results["general"]
    except:
        pass

    return results
    # df = pd.DataFrame(results)
    # df.to_csv('messari_asset_details_graphql.csv',index=False)

    
    
if __name__ == "__main__":
    # get_mesasri_assets_algolia()
    df = pd.read_csv('messari_scraper.csv')
    slugs = df['slug'].tolist()
    print(len(slugs))
    results = []
    for slug in slugs[:5]:
        results.append(get_messari_asset_details_graphql(slug))
    df = pd.DataFrame(results)
    df.to_csv('messari_asset_details_graphql.csv',index=False)