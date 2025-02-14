import os
import json
import datetime
import urllib.parse


import requests
from bs4 import BeautifulSoup, SoupStrainer

from letzegensuchen import taz

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}

TAZ_BASE_URL = "https://taz.de"
TAZ_QUERY_PATH = '!s="letzte+generation"'
TAZ_KEYWORD_SEARCH_URL = urllib.parse.urljoin(TAZ_BASE_URL, TAZ_QUERY_PATH)


def uniqify(seq):
    return list(dict.fromkeys(seq))


def main():
    print(TAZ_KEYWORD_SEARCH_URL)
    links = get_search_links(TAZ_KEYWORD_SEARCH_URL)
    # save_search_results(links)
    # r = requests.get(TAZ_KEYWORD_SEARCH_URL)
    # s = BeautifulSoup(
    #     r.content,
    #     "html.parser",
    #     parse_only=SoupStrainer("a"),
    # )
    # hrefs = [tag["href"] for tag in s.find_all("a", attrs={"class": "teaser-link"})]
    # print("base results:")
    # print(len(hrefs), hrefs, end="\n")
    # print("unique results:")
    # unique_hrefs = uniqify(hrefs)
    # print(len(unique_hrefs), unique_hrefs)


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
