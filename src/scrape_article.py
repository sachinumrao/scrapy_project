import json
import re

import pandas as pd
from bs4 import BeautifulSoup
from gazpacho import Soup, get
from retry import retry
from tqdm.auto import tqdm

# from typing import deprecated


URLMAP_FILE = "./investopedia_all_urls.json"
CONTENT_FILE = "./../data/investopedia.csv"


def clean_content(content: str) -> str:
    # remove additional newlines
    cln_text = re.sub(r"\n+", "\n", content).strip()

    # remove additional white spaces
    return cln_text


@retry(tries=10, delay=5)
def gazpacho_extract_content(url):
    page = get(url)
    soup = Soup(page)
    div_pattern = "mntl-sc-page_1-0"
    div = soup.find("div", {"id": div_pattern})
    question = div.text

    s = BeautifulSoup(page, "html.parser")
    d = s.find("div", {"id": div_pattern})
    content = d.get_text()

    cln_content = clean_content(content)

    return question, cln_content


def save_content(topic2text):
    df = pd.DataFrame(topic2text, columns=["Topic", "Question", "Text"])
    df["DocID"] = df.index
    df.to_csv(CONTENT_FILE, index=False)
    print("content saved successfully")


def main():
    topic2text = []
    url_tups = []
    # http = urllib3.PoolManager()
    # load url map
    with open(URLMAP_FILE, "r") as f:
        url_map = json.load(f)

    for url_data in url_map.values():
        for url_ in url_data:
            topic = url_["topic"]
            url = url_["url"]
            url_tups.append((topic, url))

    print("total topics: ", len(url_tups))

    topic2text = []
    pbar = tqdm(url_tups, smoothing=0.9)
    for topic, url in pbar:
        pbar.set_description(topic[:20] + "...")
        question, text = gazpacho_extract_content(url)
        topic2text.append((topic, question, text))

    save_content(topic2text)


if __name__ == "__main__":
    main()
