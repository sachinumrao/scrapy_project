import json
from urllib.request import urlopen

from bs4 import BeautifulSoup
from tqdm.auto import tqdm

LETTER2URLS = "./investopedia_all_urls.json"


def get_page(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    return soup


def get_all_articles(page_soup):
    """
    function returns list of relevant article links with id pattern:
    'dictionary-top300-list__*''
    """

    url_data = []
    pattern = "dictionary-top300-list__"

    # get all anchor tage with id pattern
    tags = page_soup.find_all(
        "a", {"id": lambda x: x and x.startswith(pattern)}
    )

    # extract urls and topic names from anchor tags
    for tag in tags:
        topic = tag.string
        url = tag.get("href")

        if url.endswith(".asp"):
            url_data.append({"topic": topic, "url": url})

    return url_data


def save_url_mappings(url_mappings):
    with open(LETTER2URLS, "w") as f:
        json.dump(url_mappings, f, indent=4)

    print("url mapping saved succefully")


def main():
    letter2items = {}  # save mapping of letter to all relevant urls

    letters = [
        "num",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    numbers = [4769350 + i for i in range(len(letters))]

    for letter, letter_id in tqdm(zip(letters, numbers), total=len(letters)):
        full_url = "https://www.investopedia.com/"
        full_url += f"terms-beginning-with-{letter}-{str(letter_id)}"

        url_soup = get_page(full_url)
        # url_soup = get_page(
        #     "https://www.investopedia.com/terms-beginning-with-num-4769350"
        # )

        letter2items[letter] = get_all_articles(url_soup)

    save_url_mappings(letter2items)


if __name__ == "__main__":
    main()
