from typing import TypedDict


class Tag(TypedDict):
    id: str
    name: str


class Article(TypedDict):
    id: str
    headline: str
    description: str
    date_published: str
    authors: list[str]
    tags: list[Tag]
    text: str
