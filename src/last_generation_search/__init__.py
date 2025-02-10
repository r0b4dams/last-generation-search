import re
import json
import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, SoupStrainer


TAZ_BASE_URL = "https://taz.de"
TAZ_QUERY_PATH = '!s="letzte+generation"'

test_article_url = "https://taz.de/Haus-der-Offiziere/!6063313/"


def search_str():
    link_arr = []
    curr_url = urljoin(TAZ_BASE_URL, TAZ_QUERY_PATH)

    while True:
        response = requests.get(curr_url)
        soup = BeautifulSoup(response.text, "html.parser", parse_only=SoupStrainer("a"))

        href_set = set()

        for a_tag in soup.find_all("a", attrs={"class": "teaser-link"}):
            href = a_tag["href"]

            if href in href_set:
                continue
            else:
                link = f"{TAZ_BASE_URL}{a_tag['href']}"
                link_arr.append(link)
                href_set.add(href)

        if next_page := soup.find("a", attrs={"class": "pagination-next"}):
            curr_url = next_page["href"]
        else:
            break

    dt = str(datetime.datetime.now()).replace(" ", "_")
    filename = f"keyword_{dt}.json"

    with open(filename, "w") as f:
        json.dump(link_arr, f, indent=2)

    print("complete")


def get_TAZ_article_id(url: str) -> str | None:
    """
    Given a url, return the article's id

    In TAZ URL paths, an article id is a sequence of digits prefixed by '!'
    """
    if result := re.search(r"!(\d+)", url):
        return result.group(1)
    return None


def parse_page(url):
    """
    topline: .typo-r-topline-detail, .typo-topline
    headline: .typo-r-head-detail, .typo-head-extra-large
    subline: .typo-r-subline-detail

    ##### date and time are wrapped in <time /> tags
    date: .meta-data-container > time [0]
    time: .meta-data-container > time [1]

    Maybe instead we grab metadata from the <meta/> tags from <head>?

    use this to grab
    document.querySelector("meta[name='taz:title']")

    <meta property="og:title" content="{topline}:{headline}"
    <meta property="og:description" content="{description}"
    <meta property="article:published_time" content="{dt}">
    <meta property="og:locale" content="de_DE">
    """

    response = requests.get(url)
    soup = BeautifulSoup(
        response.text,
        "html.parser",
        parse_only=SoupStrainer("meta"),
        # response.text, "html.parser", parse_only=SoupStrainer(["meta", "article"])
    )
    data = {}

    title_meta = soup.select_one("meta[name='taz:title']")

    id = title_meta["data-id"]
    topline, headline = title_meta["content"].split(":")

    data["id"] = id
    data["topline"] = format_str(topline)
    data["headline"] = format_str(headline)

    print(data)

    # article_id = get_TAZ_article_id(url)
    # strainer = SoupStrainer("article")
    # text = soup.find("article").get_text()
    # with open(f"{article_id}.txt", "w") as f:
    #     f.write(text)


def format_str(string: str):
    """
    Remove zero-width spaces and trim whitespace
    """
    return string.replace("\u200b", "").strip()


def main() -> None:
    # search_str()
    parse_page(test_article_url)
