import os
import json
import datetime
import urllib.parse


import requests
from bs4 import BeautifulSoup, SoupStrainer

from letzegensuchen import taz, user_agent

HEADERS = {"User-Agent": user_agent.win10_edge}

TAZ_BASE_URL = "https://taz.de"
TAZ_QUERY_PATH = '!s="letzte+generation"'
TAZ_KEYWORD_SEARCH_URL = urllib.parse.urljoin(TAZ_BASE_URL, TAZ_QUERY_PATH)


def uniqify(seq):
    return list(dict.fromkeys(seq))


def main():
    print(TAZ_KEYWORD_SEARCH_URL)
    print(HEADERS)


def save_search_results(links: list[str]) -> None:
    os.makedirs("articles", exist_ok=True)
    total_links = len(links)
    for i, link in enumerate(links):
        print(f"saving page {i + 1} of {total_links} at {link}")

        try:
            response = requests.get(link, headers=HEADERS)

        except requests.exceptions.TooManyRedirects:
            print("Encountered TooManyRedirects exception")
            print("Error accessing", link)

        page = taz.PageScraper(response.text)

        id = page.article["id"]
        dt = page.article["date_published"]

        if text := page.article["text"]:
            filename = f"articles/{dt}_{id}.txt"
            with open(filename, "w") as f:
                f.write(text)
        else:
            print(f"skipping article {id} - no text")


def get_search_links() -> list[str]:
    page_no = 1
    link_arr = []
    current_url = TAZ_KEYWORD_SEARCH_URL

    while True:
        print(f"scraping page {page_no}")
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, "html.parser", parse_only=SoupStrainer("a"))

        href_set = set()

        for a_tag in soup.find_all("a", attrs={"class": "teaser-link"}):
            href = a_tag["href"]
            # NOTE: this is O(n^2)
            if href in href_set:
                continue
            else:
                link = urllib.parse.urljoin(TAZ_BASE_URL, a_tag["href"])
                link_arr.append(link)
                href_set.add(href)

        if next_page := soup.find("a", attrs={"class": "pagination-next"}):
            current_url = next_page["href"]
            page_no += 1
        else:
            break

    dt = str(datetime.datetime.now()).replace(" ", "_")
    filename = f"keyword_{dt}.json"
    with open(filename, "w") as f:
        json.dump(link_arr, f, indent=2)

    print("link scrape completed")
    return link_arr
