import json
import re

import pandas as pd
import urllib3
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

URLMAP_FILE = "./investopedia_all_urls.json"
CONTENT_FILE = "./investopedia.csv"


def clean_content(content: str) -> str:
    # remove additional newlines
    cln_text = re.sub(r"\n+", "\n", content).strip()

    # remove additional white spaces
    return cln_text


def extract_content(page):
    # topic, url = url_tup
    # page = urlopen(url)
    html = page.data.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    div_pattern = "mntl-sc-page_1-0"
    div = soup.find("div", {"id": div_pattern})
    content = div.get_text()

    cln_content = clean_content(content)

    return cln_content


def save_content(topic2text):
    df = pd.DataFrame(topic2text, columns=["Topic", "Text"])
    df["DocID"] = df.index
    df.to_csv(CONTENT_FILE, index=False)
    print("content saved successfully")


def main():
    topic2text = []
    url_tups = []
    http = urllib3.PoolManager()
    # load url map
    with open(URLMAP_FILE, "r") as f:
        url_map = json.load(f)

    for url_data in url_map.values():
        for url_ in url_data:
            topic = url_["topic"]
            url = url_["url"]
            url_tups.append((topic, url))

    print("total topics: ", len(url_tups))

    print("getting source pages...")
    topic2page = []
    for topic, url in tqdm(url_tups, total=len(url_tups)):
        print(url)
        topic2page.append((topic, http.request("GET", url)))

    print("extratcing page content...")
    topic2text = [
        (topic, extract_content(page))
        for topic, page in tqdm(topic2page, total=len(topic2page))
    ]

    save_content(topic2text)


if __name__ == "__main__":
    main()
