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

def get_courses(pagenumber,category_id):
    url = "https://www.udemy.com/api-2.0/discovery-units/all_courses/?p={}&page_size=60&subcategory=&instructional_level=&lang=&price=&duration=&closed_captions=&subs_filter_type=&label_id={}&source_page=topic_page&locale=en_US&currency=eur&navigation_locale=en_US&skip_price=true&sos=pl&fl=lbl".format(str(pagenumber),str(category_id))
    response = requests.get(url,proxies=proxies)
    results = response.json()
    return results

def get_all_courses():
    category_id = 7380
    results = []
    i = 1
    while True:
        print("Getting page {}".format(i))
        try:
            res =  get_courses(i,category_id)
            if "detail" in res.keys():
                break
            results += res["unit"]["items"]
        except Exception as e:
            print(e)
        i += 1
        if i > 1000:
            break

    df = pd.DataFrame(results)
    df.to_csv("udemy_courses.csv",index=False)


if __name__ == "__main__":
    # results = get_courses(1,7380)
    # print(results)
    get_all_courses()

