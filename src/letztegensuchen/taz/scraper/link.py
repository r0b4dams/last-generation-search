from bs4 import BeautifulSoup, SoupStrainer
import requests

class LinkScraper(BeautifulSoup):
    def __init__(self, search_phrase, weekend_only):
        pass