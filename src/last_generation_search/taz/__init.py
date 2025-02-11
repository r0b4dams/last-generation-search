from bs4 import BeautifulSoup, ResultSet, Tag


def get_id_headline(soup: BeautifulSoup):
    meta = soup.select_one('meta[name="taz:title"]')
    id = meta["data-id"]
    hl = meta["content"]
    return id, hl


def get_description(soup: BeautifulSoup) -> str:
    meta = soup.select_one('meta[name="description"]')
    desc = meta["content"]
    return desc


def get_dt(soup: BeautifulSoup) -> str:
    meta = soup.select_one('meta[property="article:published_time"]')
    dt = meta["content"]
    return dt


def get_authors(soup: BeautifulSoup) -> list[str]:
    meta_set = soup.select('meta[property="article:author"]')
    authors = [meta["content"] for meta in meta_set]
    # TODO: add fallback in case no auth meta tags
    return authors


def get_tags(soup: BeautifulSoup) -> list[dict[str, str]]:
    meta_set = soup.select('meta[property="article:tag"]')
    tags = [{"id": meta["data-tag-id"], "name": meta["content"]} for meta in meta_set]
    return tags


def get_text(soup: BeautifulSoup) -> str: ...
