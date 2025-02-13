from urllib.parse import urljoin
from pprint import pp

import requests

from letzegensuchen import taz


TAZ_BASE_URL = "https://taz.de"
TAZ_QUERY_PATH = '!s="letzte+generation"'
TAZ_KEYWORD_SEARCH_URL = urljoin(TAZ_BASE_URL, TAZ_QUERY_PATH)

test_article_url = "https://taz.de/Haus-der-Offiziere/!6063313/"


def main():
    res = requests.get(test_article_url)
    page = taz.PageScraper(res.text)
    pp(page.article)
