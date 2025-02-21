import urllib.parse


from narrative_futures.utils import date

TAZ_BASE_URL = "https://taz.de"


def build_search_url(query: str, weekend_only: bool, start_date: str):
    normalized_query = query.strip().replace(" ", "+")

    if not normalized_query:
        raise Exception("invalid query")

    path = [f'!s="{normalized_query}"']

    if weekend_only:
        path.append("isWochenende=1")

    if start_date:
        if not date.is_valid(start_date):
            raise Exception("invalid date format:", start_date)
        path.append("eTagAb=" + start_date)

    return urllib.parse.urljoin(TAZ_BASE_URL, "&".join(path))
