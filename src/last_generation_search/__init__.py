import re
import json
import datetime

import requests
from bs4 import BeautifulSoup, SoupStrainer


TAZ_BASE_URL = "https://taz.de"
TAZ_STR_QUERY = '"letzte+generation"'


def search_str():
    link_arr = []
    current_url = f"{TAZ_BASE_URL}/!s={TAZ_STR_QUERY}"

    while True:
        response = requests.get(current_url)
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
            current_url = next_page["href"]
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


def main() -> None:
    search_str()
